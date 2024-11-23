import os
from typing import Any, Dict, List, Optional, Type
from datetime import datetime, timezone
from decouple import config
from uuid import UUID
from sqlmodel import select, SQLModel, Session, create_engine
import sqlalchemy as sa
from sqlalchemy import or_, func

url = config("DATABASE_URL")

engine = create_engine(url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def schema():
    "Show all tables and columns"
    inspector = sa.inspect(engine)
    res = ""
    for table_name in inspector.get_table_names():
        res += f"Table: {table_name}\n"
        pk_cols = inspector.get_pk_constraint(table_name)["constrained_columns"]
        for column in inspector.get_columns(table_name):
            pk_marker = "*" if column["name"] in pk_cols else "-"
            res += f"  {pk_marker} {column['name']}: {column['type']}\n"
    return res


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_model_fields(model: Type[SQLModel]) -> List[str]:
    return list(model.__fields__.keys())


def all_records(model: Type[SQLModel]) -> List[SQLModel]:
    with Session(engine) as session:
        result = session.exec(select(model)).all()

    return result


def query_records(
    model: Type[SQLModel],
    search_value: Optional[str] = None,
    sorting_field: Optional[str] = None,
    sort_direction: str = "asc",
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    as_dict: bool = False,
    fields: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    with Session(engine) as session:
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


def get_record(
    model: Type[SQLModel], id: Any, alt_key: str = None
) -> Optional[SQLModel]:
    with Session(engine) as session:
        if alt_key:
            stmt = select(model).where(getattr(model, alt_key) == id)
            result = session.exec(stmt).first()
        else:
            if isinstance(id, str):
                id = UUID(id)
            result = session.get(model, id)
        return result


def update_record(
    model: Type[SQLModel], id: Any, data: Dict[str, Any]
) -> Dict[str, Any]:
    with Session(engine) as session:
        db_record = session.get(model, id)
        if db_record:
            for key, value in data.items():
                setattr(db_record, key, value)
            session.add(db_record)
            session.commit()
            session.refresh(db_record)

            return db_record.dict()
        else:
            raise Exception("Record not found")


def delete_record(model: Type[SQLModel], id: Any) -> None:
    with Session(engine) as session:
        db_record = session.get(model, id)
        if db_record:
            session.delete(db_record)
            session.commit()

        else:
            raise Exception("Record not found")


def upsert_record(model: Type[SQLModel], data: Dict[str, Any]) -> SQLModel:
    with Session(engine) as session:
        if "id" in data:
            if isinstance(data["id"], str):
                data["id"] = UUID(data["id"])
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


def bulk_insert(model: Type[SQLModel], data: List[Dict[str, Any]]) -> List[SQLModel]:
    with Session(engine) as session:
        db_records = [model(**item) for item in data]
        session.add_all(db_records)
        session.commit()
        for record in db_records:
            session.refresh(record)

        return db_records


def bulk_update(model: Type[SQLModel], data: List[Dict[str, Any]]) -> List[SQLModel]:
    with Session(engine) as session:
        updated_records = []
        for item in data:
            if "id" in item:
                db_record = session.get(model, item["id"])
                if db_record:
                    for key, value in item.items():
                        setattr(db_record, key, value)
                    updated_records.append(db_record)
        session.add_all(updated_records)
        session.commit()
        for record in updated_records:
            session.refresh(record)

        return updated_records


def count_records(model: Type[SQLModel]) -> int:
    with Session(engine) as session:
        return session.exec(select(func.count()).select_from(model)).one()
