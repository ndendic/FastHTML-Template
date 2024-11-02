from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON

# from dataclasses import dataclass, field
from sqlmodel import Field

from ..base import BaseTable


class User(BaseTable, table=True):
    email: str = Field(nullable=False)
    password: str = Field(default="")
    role: str = Field(default="authenticated")
    is_admin: bool = Field(default=False)
    user_metadata: Dict[str, Any] = Field(sa_column=Column(JSON))
    confirmed_at: Optional[datetime] = None
    email_confirmed_at: Optional[datetime] = None
    last_sign_in_at: Optional[datetime] = None

    table_fields = ["id", "email", "first_name", "last_name", "is_admin"]

    @classmethod
    def get_by_email(cls, email: str) -> "User":
        return cls.get(id=email, alt_key="email")
