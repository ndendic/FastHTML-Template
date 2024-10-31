import os
from typing import Any, Dict, List, Optional, Type
from datetime import datetime, timezone
from decouple import config

from sqlmodel import select, SQLModel, Session, create_engine
import sqlalchemy as sa
from sqlalchemy import or_, func
from .supabase import supabase


def get_backend():
    if os.environ.get("SUPABASE_KEY"):
        return "sqlmodel"
        # return "supabase"
    else:
        return "sqlmodel"


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
    backend = get_backend()

    if backend == "supabase":
        response = supabase.table(model.__name__.lower()).select("*").execute()
        data: List[dict] = response.data
        result = model._cast_data(data)
    else:  # sqlmodel
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
    backend = get_backend()
    if backend == "supabase":
        table_name = model.__tablename__

        if fields:
            fields_string = ",".join(fields)
            query = supabase.table(table_name).select(fields_string)
        else:
            query = supabase.table(table_name).select("*")

        if search_value:
            string_fields = [
                field.name for field in model.__fields__.values() if field.type_ is str
            ]
            if string_fields:
                conditions = [
                    f"{field}.ilike.*{search_value}*" for field in string_fields
                ]
                or_condition = ",".join(conditions)
                query = query.or_(or_condition)

        if sorting_field:
            if sorting_field in model.__fields__:
                desc = sort_direction.lower() == "desc"
                query = query.order(sorting_field, desc=desc)
            else:
                raise ValueError(
                    f"Sorting field '{sorting_field}' does not exist in the model."
                )
        else:
            query = query.order("id")

        if limit is not None and offset is not None:
            end = offset + limit - 1
            query = query.range(offset, end)

        try:
            response = query.execute()
            if as_dict:
                return response.data or []
            else:
                return model._cast_data(data=response.data) or []
        except Exception as e:
            raise Exception(f"Error querying records: {str(e)}")
    else:  # sqlmodel
        with Session(engine) as session:
            if fields:
                query = select(*[getattr(model, field) for field in fields])
            else:
                query = select(model)

            if search_value:
                string_fields = [
                    field.name
                    for field in model.__fields__.values()
                    if field.type_ is str
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
                return [result.dict() for result in results]
            else:
                return results


def get_record(
    model: Type[SQLModel], id: Any, alt_key: str = None
) -> Optional[SQLModel]:
    backend = get_backend()
    if backend == "supabase":
        table_name = model.__tablename__
        try:
            key = "id" if not alt_key else alt_key
            response = supabase.table(table_name).select("*").eq(key, id).execute()
            if response.data:
                return model(**response.data[0])
            else:
                return None
        except Exception as e:
            raise Exception(f"Error fetching record: {str(e)}")
    else:  # sqlmodel
        with Session(engine) as session:
            if alt_key:
                stmt = select(model).where(getattr(model, alt_key) == id)
                result = session.exec(stmt).first()
            else:
                result = session.get(model, id)
            return result


def update_record(
    model: Type[SQLModel], id: Any, data: Dict[str, Any]
) -> Dict[str, Any]:
    backend = get_backend()
    if backend == "supabase":
        table_name = model.__tablename__
        valid_fields = get_model_fields(model)
        update_data = {k: v for k, v in data.items() if k in valid_fields}

        if not update_data:
            raise ValueError("No valid fields provided for update.")

        try:
            response = (
                supabase.table(table_name).update(update_data).eq("id", id).execute()
            )
            if response.data:
                return response.data[0]
            else:
                raise Exception("Record not found or update failed.")
        except Exception as e:
            raise Exception(f"Error updating record: {str(e)}")
    else:  # sqlmodel
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
    backend = get_backend()
    if backend == "supabase":
        table_name = model.__tablename__
        try:
            response = supabase.table(table_name).delete().eq("id", id).execute()
            if not response.data:
                raise Exception("Record not found or delete failed.")
        except Exception as e:
            raise Exception(f"Error deleting record: {str(e)}")
    else:  # sqlmodel
        with Session(engine) as session:
            db_record = session.get(model, id)
            if db_record:
                session.delete(db_record)
                session.commit()

            else:
                raise Exception("Record not found")


def upsert_record(model: Type[SQLModel], data: Dict[str, Any]) -> SQLModel:
    backend = get_backend()
    if backend == "supabase":
        table_name = model.__tablename__
        valid_fields = get_model_fields(model)
        upsert_data = {k: v for k, v in data.items() if k in valid_fields}

        if not upsert_data:
            raise ValueError("No valid fields provided for upsert.")
        try:
            response = supabase.table(table_name).upsert(upsert_data).execute()
            if response.data:
                return model._cast_data(response.data)[0]
            else:
                raise Exception("Upsert failed.")
        except Exception as e:
            raise Exception(f"Error upserting record: {str(e)}")
    else:  # sqlmodel
        with Session(engine) as session:
            if "id" in data:
                db_record = session.get(model, data["id"])
                if db_record:
                    for key, value in data.items():
                        setattr(db_record, key, value)
                else:
                    db_record = model(**data)
            else:
                db_record = model(**data)

            session.add(db_record)
            session.commit()
            session.refresh(db_record)

            return db_record


def bulk_insert(model: Type[SQLModel], data: List[Dict[str, Any]]) -> List[SQLModel]:
    backend = get_backend()
    if backend == "supabase":
        table_name = model.__tablename__
        try:
            response = supabase.table(table_name).insert(data).execute()
            if response.data:
                return model._cast_data(response.data)
            else:
                raise Exception("Bulk insert failed.")
        except Exception as e:
            raise Exception(f"Error during bulk insert: {str(e)}")
    else:  # sqlmodel
        with Session(engine) as session:
            db_records = [model(**item) for item in data]
            session.add_all(db_records)
            session.commit()
            for record in db_records:
                session.refresh(record)

            return db_records


def bulk_update(model: Type[SQLModel], data: List[Dict[str, Any]]) -> List[SQLModel]:
    backend = get_backend()
    if backend == "supabase":
        table_name = model.__tablename__
        try:
            response = supabase.table(table_name).upsert(data).execute()
            if response.data:
                return model._cast_data(response.data)
            else:
                raise Exception("Bulk update failed.")
        except Exception as e:
            raise Exception(f"Error during bulk update: {str(e)}")
    else:  # sqlmodel
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
    backend = get_backend()
    if backend == "supabase":
        table_name = model.__tablename__
        try:
            response = supabase.table(table_name).select("*", count="exact").execute()
            return response.count
        except Exception as e:
            raise Exception(f"Error counting records: {str(e)}")
    else:  # sqlmodel
        with Session(engine) as session:
            return session.exec(select(func.count()).select_from(model)).one()
