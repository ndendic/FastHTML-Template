from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, Relationship

# from dataclasses import dataclass, field
from modules.shared.models import BaseTable


class RolePriviledge(BaseTable, table=True):
    role_name: str = Field(
        foreign_key="role.name",
        nullable=False,
        title="Role",
        schema_extra={
            "icon": "key-round",
            "input_type": "select",
            "related_model": "Role",
            "related_field": "name",
        },
    )
    priviledge_name: str = Field(
        foreign_key="priviledge.name",
        nullable=False,
        title="Priviledge",
        schema_extra={
            "icon": "key-round",
            "input_type": "select",
            "related_model": "Priviledge",
            "related_field": "name",
        },
    )

    display_name = "Role Priviledges"
    sidebar_item = True
    detail_page_title = "Role Priviledge"
    default_sort_field = "role_name"
    table_view_fields = ["role_name", "priviledge_name", "created_at", "updated_at"]
    detail_page_fields = ["role_name", "priviledge_name"]
    sidebar_icon = "key-round"

    # __table_args__ = (PrimaryKeyConstraint("role_name", "priviledge_name"),)

    def __str__(self):
        return f"{self.role_name} - {self.priviledge_name}"

    def __repr__(self):
        return f"{self.role_name} - {self.priviledge_name}"


class User(BaseTable, table=True):
    email: str = Field(nullable=False, unique=True, schema_extra={"input_type": "email"})
    full_name: Optional[str] = Field(nullable=True, title="Full Name")
    avatar_url: Optional[str] = Field(nullable=True, title="Avatar")
    password: Optional[str] = Field(nullable=True, default="")
    role: Optional[str] = Field(foreign_key="role.name", default="authenticated")
    is_admin: Optional[bool] = Field(default=False)
    user_metadata: Optional[Dict[str, Any]] = Field(
        sa_column=Column(JSON), schema_extra={"input_type": "json"}
    )
    confirmed_at: Optional[datetime] = Field(schema_extra={"input_type": "date"})
    email_confirmed_at: Optional[datetime] = None
    last_sign_in_at: Optional[datetime] = None

    # * Relationships
    roles: Optional["Role"] = Relationship(back_populates="users")

    # * Class Medatadata
    table_view_fields = ["id", "email", "full_name", "is_admin", "role"]
    detail_page_fields = ["full_name", "email", "is_admin", "role"]
    detail_page_title = "User Details"
    field_groups = {
        "Basic Information": ["full_name", "email"],
        "Account Settings": ["is_admin", "role"],
    }
    display_name = "Users"
    sidebar_icon = "user"

    @classmethod
    def get_by_email(cls, email: str) -> "User":
        return cls.get(id=email, alt_key="email")

    @property
    def priviledges(self) -> list[str]:
        privileges: dict = RolePriviledge.query(
            search_value=self.role,
            fields=["priviledge_name"],  # Assuming the field is named 'privilege_name'
            as_dict=True,
        )

        # Extract privilege names from the results
        privilege_names = [
            item["priviledge_name"]
            for item in privileges
            if item.get("priviledge_name")
        ]

        return privilege_names


class Role(BaseTable, table=True):
    name: str = Field(
        index=True,
        unique=True,
        nullable=False,
        title="Role Name",
        schema_extra={"icon": "key_round"},
    )
    product_name: str = Field(
        nullable=True,
        title="Product Name",
        description="The name of the product associated with this role",
    )
    description: Optional[str] = Field(nullable=True, title="Description")

    # * Relationships
    users: List["User"] = Relationship(back_populates="roles")
    priviledges: List["Priviledge"] = Relationship(
        back_populates="roles", link_model=RolePriviledge
    )

    # * Class Metadata
    display_name = "Roles"
    sidebar_item = True
    detail_page_title = "Role"
    table_view_fields = [
        "name",
        "product_name",
        "description",
        "created_at",
        "updated_at",
    ]
    detail_page_fields = ["name", "product_name", "description"]
    sidebar_icon = "key-round"

    @property
    def priviledge_names(self) -> List[str]:
        return [priviledge.priviledge_name for priviledge in self.priviledges]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Priviledge(BaseTable, table=True):
    name: str = Field(
        index=True,
        unique=True,
        nullable=False,
        title="Priviledge Name",
        schema_extra={"icon": "key_round"},
    )
    description: Optional[str] = Field(nullable=True, title="Description")
    roles: List[Role] = Relationship(
        back_populates="priviledges", link_model=RolePriviledge
    )

    display_name = "Priviledges"
    sidebar_item = True
    detail_page_title = "Priviledge"
    table_view_fields = ["name", "description", "created_at", "updated_at"]
    detail_page_fields = ["name", "description"]
    sidebar_icon = "key-round"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
