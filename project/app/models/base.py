from datetime import datetime, timezone
from typing import ClassVar, Any, Dict, Optional, List, Set
from uuid import uuid4, UUID
import sqlalchemy

# from fastsql import Database, DBTable
from sqlmodel import SQLModel, Field
from ..services.db import db


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseTable(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
        title="Created At",
        schema_extra={"icon": "clock", "rx_input_type": "datetime"},
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
        title="Updated At",
        schema_extra={"icon": "clock", "rx_input_type": "datetime"},
    )

    db_xtra: ClassVar[dict] = {}
    sidebar_item: ClassVar[bool] = True
    table_fields: ClassVar[list[str]] = ["id"]

    @classmethod
    def related_records(cls) -> dict[str, List]:
        pass

    @classmethod
    def all(cls) -> List["BaseTable"]:
        return db.all_records(cls)

    @classmethod
    def query(
        cls,
        search_value: Optional[str] = None,
        sorting_field: Optional[str] = None,
        sort_direction: str = "asc",
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        as_dict: bool = False,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        return db.query_records(
            cls,
            search_value=search_value,
            sorting_field=sorting_field,
            sort_direction=sort_direction,
            limit=limit,
            offset=offset,
            as_dict=as_dict,
            fields=fields,
        )

    @classmethod
    def get(cls, id: Any, alt_key: str = None) -> Optional["BaseTable"]:
        return db.get_record(cls, id, alt_key)

    @classmethod
    def update(cls, id: Any, data: Dict[str, Any]) -> Dict[str, Any]:
        return db.update_record(cls, id, data)

    @classmethod
    def delete(cls, id: Any) -> None:
        db.delete_record(cls, id)

    @classmethod
    def upsert(cls, data: Dict[str, Any]) -> "BaseTable":
        return db.upsert_record(cls, data)

    def save(self) -> "BaseTable":
        return db.upsert_record(self.__class__, self.dict())

    def dict(self, *args, **kwargs):
        return self._dict_with_custom_encoder(set(), *args, **kwargs)

    def _dict_with_custom_encoder(self, processed: Set[int], *args, **kwargs):
        if id(self) in processed:
            return {"id": getattr(self, "id", None)}

        processed.add(id(self))

        data = {}
        for field in self.model_fields:
            value = getattr(self, field)
            if isinstance(value, BaseTable):
                value = value._dict_with_custom_encoder(processed, *args, **kwargs)
            elif isinstance(value, list):
                value = [
                    item._dict_with_custom_encoder(processed, *args, **kwargs)
                    if isinstance(item, BaseTable)
                    else item
                    for item in value
                ]
            elif isinstance(value, dict):
                value = {
                    k: v._dict_with_custom_encoder(processed, *args, **kwargs)
                    if isinstance(v, BaseTable)
                    else v
                    for k, v in value.items()
                }
            elif isinstance(value, datetime):
                value = value.isoformat()

            data[field] = value

        return data


# db.create(User)
