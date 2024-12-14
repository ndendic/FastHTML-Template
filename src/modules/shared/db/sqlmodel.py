from typing import Any, Dict, Generator, List, Optional, Type
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy import func, or_
from sqlmodel import Session, SQLModel, create_engine, select
from uuid import UUID

from modules.shared.db.base import DatabaseService
def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class SQLModelDB(DatabaseService):
    def __init__(self, url: str):
        self.engine = create_engine(url, echo=True)

    def init_db(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session

    def schema(self) -> str:
        inspector = sa.inspect(self.engine)
        res = ""
        for table_name in inspector.get_table_names():
            res += f"Table: {table_name}\n"
            pk_cols = inspector.get_pk_constraint(table_name)["constrained_columns"]
            for column in inspector.get_columns(table_name):
                pk_marker = "*" if column["name"] in pk_cols else "-"
                res += f"  {pk_marker} {column['name']}: {column['type']}\n"
        return res

    def all_records(self, model: Type[SQLModel]) -> List[SQLModel]:
        with Session(self.engine) as session:
            statement = select(model)
            results = session.exec(statement).all()
            return results

    def query_records(
        self,
        model: Type[SQLModel],
        search_value: Optional[str] = None,
        sorting_field: Optional[str] = None,
        sort_direction: str = "asc",
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        as_dict: bool = False,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        with Session(self.engine) as session:
            if fields:
                query = select(*[getattr(model, field) for field in fields])
            else:
                query = select(model)

            if search_value:
                string_fields = [
                    k for k, v in model.__fields__.items() if v.annotation is str
                ]
                if string_fields:
                    conditions = [
                        getattr(model, field).ilike(f"%{search_value}%")
                        for field in string_fields
                    ]
                    query = query.filter(or_(*conditions))

            if sorting_field:
                if sorting_field in model.__fields__:
                    order_field = getattr(model, sorting_field)
                    query = query.order_by(
                        order_field.desc()
                        if sort_direction.lower() == "desc"
                        else order_field
                    )
                else:
                    raise ValueError(
                        f"Sorting field '{sorting_field}' does not exist in the model."
                    )
            else:
                query = query.order_by(model.id)

            if limit is not None:
                query = query.limit(limit)

            if offset is not None:
                query = query.offset(offset)

            results = session.exec(query).all()

            if as_dict:
                dict_results = [result._asdict() for result in results]
                return dict_results
            else:
                return results

    # Add to SQLModelDB class in sqlmodel.py

    def get_record(
        self, model: Type[SQLModel], id: Any, alt_key: str = None
    ) -> Optional[SQLModel]:
        with Session(self.engine) as session:
            if alt_key:
                stmt = select(model).where(getattr(model, alt_key) == id)
                result = session.exec(stmt).first()
            else:
                if isinstance(id, str):
                    id = UUID(id)
                result = session.get(model, id)
            return result

    def update_record(
        self, model: Type[SQLModel], id: Any, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        with Session(self.engine) as session:
            record = session.get(model, id)
            if not record:
                raise Exception(f"Record with id {id} not found")
            for key, value in data.items():
                setattr(record, key, value)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.dict()

    def delete_record(self, model: Type[SQLModel], id: Any) -> None:
        with Session(self.engine) as session:
            record = session.get(model, id)
            if record:
                session.delete(record)
                session.commit()


    def upsert_record(self, model: Type[SQLModel], data: Dict[str, Any]) -> SQLModel:
        with Session(self.engine) as session:
            if "id" in data:
                if isinstance(data["id"], str):
                    data["id"] = UUID(data["id"])
                data.pop("created_at",None)
                db_record = session.get(model, data["id"])
                if db_record:
                    for key, value in data.items():
                        setattr(db_record, key, value)
                    db_record.updated_at = utc_now()
                else:
                    db_record = model(**data)
                    db_record.created_at = utc_now()
                    db_record.updated_at = utc_now()
            else:
                db_record = model(**data)
                db_record.created_at = utc_now()
                db_record.updated_at = utc_now()

            session.add(db_record)
            session.commit()
            session.refresh(db_record)

            return db_record

    def bulk_insert(
        self, model: Type[SQLModel], data: List[Dict[str, Any]]
    ) -> List[SQLModel]:
        with Session(self.engine) as session:
            records = [model(**item) for item in data]
            session.add_all(records)
            session.commit()
            for record in records:
                session.refresh(record)
            return records

    def bulk_update(
        self, model: Type[SQLModel], data: List[Dict[str, Any]]
    ) -> List[SQLModel]:
        with Session(self.engine) as session:
            records = []
            for item in data:
                if "id" in item:
                    record = session.get(model, item["id"])
                    if record:
                        for key, value in item.items():
                            setattr(record, key, value)
                        records.append(record)
            session.add_all(records)
            session.commit()
            for record in records:
                session.refresh(record)
            return records

    def count_records(self, model: Type[SQLModel]) -> int:
        with Session(self.engine) as session:
            return session.exec(select(func.count()).select_from(model)).one()
