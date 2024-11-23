from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field

from app.models.base import BaseTable


class User(BaseTable, table=True):
    email: str = Field(nullable=False)
    full_name: str = Field(nullable=True, title="Full Name")
    avatar_url: str = Field(nullable=True, title="Avatar")
    password: str = Field(default="")
    is_admin: bool = Field(default=False)
    user_metadata: Dict[str, Any] = Field(sa_column=Column(JSON))
    confirmed_at: Optional[datetime] = None
    email_confirmed_at: Optional[datetime] = None
    last_sign_in_at: Optional[datetime] = None

    table_view_fields = ["id", "email", "full_name", "is_admin"]
    detail_page_fields = ["full_name", "email", "is_admin"]
    detail_page_title = "User Details"
    field_groups = {
        "Basic Information": ["full_name", "email"],
        "Account Settings": ["is_admin", "user_metadata"],
    }
    display_name = "Users"
    sidebar_icon = "user"

    @classmethod
    def get_by_email(cls, email: str) -> "User":
        return cls.get(id=email, alt_key="email")

