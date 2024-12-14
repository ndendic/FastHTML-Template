import os

from decouple import config

from modules.shared.db.sqlmodel import SQLModelDB


def get_db_service():
    db_type = "sqlmodel"

    return SQLModelDB(url=config("DATABASE_URL"))


service = get_db_service()

__all__ = ["service"]