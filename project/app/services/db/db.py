from typing import Any, Dict, List, Optional, Type
from datetime import datetime, timezone
from decouple import config

from sqlmodel import select, SQLModel, Session, create_engine
import sqlalchemy as sa
from sqlalchemy import or_, func

url = config("DATABASE_URL")
engine = create_engine(url, echo=True)

def init_db():
    """Initialize the database by creating all tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session

def schema():
    """Show all tables and columns."""
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
    """Get current UTC timestamp."""
    return datetime.now(timezone.utc)

def get_model_fields(model: Type[SQLModel]) -> List[str]:
    """Get all field names for a model."""
    return list(model.model_fields.keys())

def all_records(model: Type[SQLModel]) -> List[SQLModel]:
    """Get all records for a model."""
    with Session(engine) as session:
        return session.exec(select(model)).all()

def convert_datetime_strings(model: Type[SQLModel], data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert ISO format datetime strings to datetime objects based on model field types."""
    converted_data = data.copy()
    for field_name, field in model.model_fields.items():
        if field_name in converted_data and isinstance(converted_data[field_name], str):
            # Get the field annotation from the model
            field_annotation = model.model_fields[field_name].annotation
            
            # Check if the field is typed as datetime
            is_datetime_field = False
            if field_annotation == datetime:
                is_datetime_field = True
            elif hasattr(field_annotation, "__origin__"):
                if field_annotation.__origin__ is Optional:
                    if datetime in field_annotation.__args__:
                        is_datetime_field = True

            if is_datetime_field:
                try:
                    # Parse the ISO format string to datetime
                    dt = datetime.fromisoformat(converted_data[field_name].replace('Z', '+00:00'))
                    # Ensure UTC timezone
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    converted_data[field_name] = dt
                except (ValueError, TypeError):
                    # If conversion fails, leave the original value
                    pass
    return converted_data

def query_records(
    model: Type[SQLModel],
    search_value: Optional[str] = None,
    sorting_field: Optional[str] = None,
    sort_direction: str = "asc",
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    as_dict: bool = False,
    fields: Optional[List[str]] = None,
) -> List[Any]:
    """Query records with filtering, sorting, and pagination."""
    with Session(engine) as session:
        if fields:
            query = select(*[getattr(model, field) for field in fields])
        else:
            query = select(model)

        if search_value:
            string_fields = [
                field_name
                for field_name, field in model.model_fields.items()
                if field.annotation == str
            ]
            if string_fields:
                conditions = [
                    getattr(model, field).ilike(f"%{search_value}%")
                    for field in string_fields
                ]
                query = query.filter(or_(*conditions))

        if sorting_field:
            if sorting_field in model.model_fields:
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
            return [result.model_dump() for result in results]
        return results

def get_record(model: Type[SQLModel], id: Any, alt_key: str = None) -> Optional[SQLModel]:
    """Get a single record by ID or alternate key."""
    with Session(engine) as session:
        if alt_key:
            stmt = select(model).where(getattr(model, alt_key) == id)
            return session.exec(stmt).first()
        return session.get(model, id)

def update_record(model: Type[SQLModel], id: Any, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a record by ID."""
    with Session(engine) as session:
        db_record = session.get(model, id)
        if db_record:
            converted_data = convert_datetime_strings(model, data)
            for key, value in converted_data.items():
                setattr(db_record, key, value)
            session.add(db_record)
            session.commit()
            session.refresh(db_record)
            return db_record.model_dump()
        raise Exception("Record not found")

def delete_record(model: Type[SQLModel], id: Any) -> None:
    """Delete a record by ID."""
    with Session(engine) as session:
        db_record = session.get(model, id)
        if db_record:
            session.delete(db_record)
            session.commit()
        else:
            raise Exception("Record not found")

def upsert_record(model: Type[SQLModel], data: Dict[str, Any]) -> SQLModel:
    """Insert or update a record."""
    with Session(engine) as session:
        # Convert any datetime strings to datetime objects
        converted_data = convert_datetime_strings(model, data)
        
        if "id" in converted_data:
            db_record = session.get(model, converted_data["id"])
            if db_record:
                for key, value in converted_data.items():
                    setattr(db_record, key, value)
            else:
                db_record = model(**converted_data)
        else:
            db_record = model(**converted_data)

        session.add(db_record)
        session.commit()
        session.refresh(db_record)
        return db_record

def bulk_insert(model: Type[SQLModel], data: List[Dict[str, Any]]) -> List[SQLModel]:
    """Insert multiple records at once."""
    with Session(engine) as session:
        converted_data = [convert_datetime_strings(model, item) for item in data]
        db_records = [model(**item) for item in converted_data]
        session.add_all(db_records)
        session.commit()
        for record in db_records:
            session.refresh(record)
        return db_records

def bulk_update(model: Type[SQLModel], data: List[Dict[str, Any]]) -> List[SQLModel]:
    """Update multiple records at once."""
    with Session(engine) as session:
        updated_records = []
        for item in data:
            if "id" in item:
                db_record = session.get(model, item["id"])
                if db_record:
                    converted_item = convert_datetime_strings(model, item)
                    for key, value in converted_item.items():
                        setattr(db_record, key, value)
                    updated_records.append(db_record)
        session.add_all(updated_records)
        session.commit()
        for record in updated_records:
            session.refresh(record)
        return updated_records

def count_records(model: Type[SQLModel]) -> int:
    """Count total records for a model."""
    with Session(engine) as session:
        return session.exec(select(func.count()).select_from(model)).one()
