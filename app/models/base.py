from datetime import datetime, timezone
from functools import lru_cache
from typing import ClassVar, Any, Dict, Optional, List, Set, Type
from uuid import uuid4, UUID
import sqlalchemy
from pydantic.fields import PydanticUndefined

# from fastsql import Database, DBTable
from sqlmodel import SQLModel, Field
from app.services.db import db

from app.components.admin_dashboard.model_table import table_page, ModelTable
from app.components.admin_dashboard.modal_form import ModalForm


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
        schema_extra={"icon": "clock", "input_type": "datetime"},
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
        title="Updated At",
        schema_extra={"icon": "clock", "input_type": "datetime"},
    )

    db_xtra: ClassVar[dict] = {}
    sidebar_item: ClassVar[bool] = True
    # Class-level metadata for frontend rendering
    display_name: ClassVar[str] = "Untitled"
    sidebar_icon: ClassVar[str] = "table"

    default_sort_field: ClassVar[str] = "id"
    table_view_fields: ClassVar[List[str]] = []
    detail_page_fields: ClassVar[List[str]] = []
    detail_page_title: ClassVar[Optional[str]] = None
    field_groups: ClassVar[Dict[str, List[str]]] = {}

    create_priviledge: ClassVar[str] = "admin"
    read_priviledge: ClassVar[str] = "admin"
    update_priviledge: ClassVar[str] = "admin"
    delete_priviledge: ClassVar[str] = "admin"

    @classmethod
    def related_records(cls) -> dict[str, List]:
        pass

    @classmethod
    def all(cls) -> List["BaseTable"]:
        return db.all_records(cls)

    @classmethod
    def total_records(cls) -> List["BaseTable"]:
        return len(db.all_records(cls))

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
    def table_view_data(cls, request) -> List[Dict[str, Any]]:
        search_value = None
        page = 1
        per_page = 10
        view_fields = cls.table_view_fields

        if "id" not in view_fields:
            view_fields.append("id")

        if hasattr(request, "query_params"):
            search_value = request.query_params.get("search_value")
            page = int(request.query_params.get("page", 1))
            per_page = int(request.query_params.get("per_page", 10))

        offset = (page - 1) * per_page

        records = cls.query(
            search_value=search_value,
            sorting_field=cls.default_sort_field,
            sort_direction="asc",
            limit=per_page,
            offset=offset,
            as_dict=True,
            fields=view_fields,
        )
        return records

    @classmethod
    def get(cls, id: Any, alt_key: str = None) -> Optional["BaseTable"]:
        return db.get_record(cls, id, alt_key)

    @classmethod
    def update_record(cls, id: Any, data: Dict[str, Any]) -> Dict[str, Any]:
        return db.update_record(cls, id, data)

    @classmethod
    def delete_record(cls, id: Any) -> None:
        db.delete_record(cls, id)

    @classmethod
    def upsert(cls, data: Dict[str, Any]) -> "BaseTable":
        return db.upsert_record(cls, data)

    @classmethod
    def _cast_data(cls, data: List[Dict[str, Any]]) -> List["BaseTable"]:
        return [cls(**item) for item in data]

    def inserted(self) -> Optional["BaseTable"]:
        if db.get_record(type(self), self.id):
            return True
        return

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

    @classmethod
    def render_table(cls, request, records_only=False):
        if records_only:
            return ModelTable(cls, request)
        else:
            return table_page(cls, request)

    @classmethod
    @lru_cache()
    def _get_model_by_name(cls, model_name: str) -> Optional[Type["BaseTable"]]:
        """Get model class by name using subclass lookup"""
        model_name = model_name.lower()
        for subclass in BaseTable.__subclasses__():
            if subclass.__name__.lower() == model_name:
                return subclass
        return None

    def _get_related_model_info(self, field_info) -> tuple:
        """Extract related model and field from foreign key"""
        if not hasattr(field_info, "foreign_key"):
            return None, None

        # foreign_key format is "model.field"
        # if hasattr(field_info,"foreign_key"):
        model_name, field_name = field_info.foreign_key.split(".")
        model_class = self._get_model_by_name(model_name)
        return model_class, field_name

    def _get_field_options(self, field_info) -> list:
        """Get options for select fields"""
        # Handle enum options
        if hasattr(field_info.annotation, "__members__"):
            return [
                {"value": member.value, "label": member.name}
                for member in field_info.annotation
            ]

        # Handle foreign key options
        if field_info.foreign_key is not PydanticUndefined:
            model_class, field_name = self._get_related_model_info(field_info)
            if model_class:
                records = model_class.all()
                return [
                    {"value": getattr(r, field_name), "label": str(r)} for r in records
                ]

        return []

    def _get_field_type(self, field_info) -> str:
        """Determine field type"""
        # Check schema_extra first
        if field_info._attributes_set and "input_type" in field_info._attributes_set:
            return field_info._attributes_set["input_type"]

        # Check for select types
        if field_info.foreign_key is not PydanticUndefined or hasattr(
            field_info.annotation, "__members__"
        ):
            return "select"

        # Standard type mapping
        type_mapping = {
            str: "text",
            int: "number",
            float: "number",
            bool: "checkbox",
            datetime: "datetime",
            UUID: "text",
            list: "select",
            dict: "json",
        }

        return type_mapping.get(field_info.annotation, "text")

    def form_data(self) -> Dict[str, Any]:
        """Generate form template"""
        model_fields = self.model_fields
        form_data = {
            "title": self.detail_page_title or self.display_name,
            "id": str(self.id) if self.id else None,
            "fields": [],
        }

        def create_field_def(field_name, field_info):
            """Helper to create field definition"""
            field_value = getattr(self, field_name, None)
            required = not getattr(field_info, "nullable", False)

            field_def = {
                "name": field_name,
                "title": field_info.title or field_name.replace("_", " ").title(),
                "type": self._get_field_type(field_info),
                "value": field_value,
                "required": required,
            }

            # Add options for select fields
            options = self._get_field_options(field_info)
            if options:
                field_def["options"] = options

            # Add schema_extra attributes
            if field_info.json_schema_extra:
                field_def.update(field_info.json_schema_extra)

            return field_def

        # Handle field groups
        if self.field_groups:
            form_data["groups"] = []
            processed_fields = set()

            for group_name, group_fields in self.field_groups.items():
                group = {"name": group_name, "fields": []}

                for field_name in group_fields:
                    if field_name in model_fields:
                        field_def = create_field_def(
                            field_name, model_fields[field_name]
                        )
                        group["fields"].append(field_def)
                        processed_fields.add(field_name)

                form_data["groups"].append(group)

            # Add ungrouped fields
            ungrouped = []
            for field_name in self.detail_page_fields:
                if field_name not in processed_fields and field_name in model_fields:
                    field_def = create_field_def(field_name, model_fields[field_name])
                    ungrouped.append(field_def)

            if ungrouped:
                form_data["fields"] = ungrouped

        # Handle flat structure
        else:
            for field_name in self.detail_page_fields:
                if field_name in model_fields:
                    field_def = create_field_def(field_name, model_fields[field_name])
                    form_data["fields"].append(field_def)

        return form_data

    def __ft__(self):
        return ModalForm(self)
