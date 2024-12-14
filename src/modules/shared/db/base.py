# db/base.py
from abc import ABC, abstractmethod
from typing import Generator, Any, Dict, List, Optional, Type
from sqlmodel import SQLModel


class DatabaseService(ABC):
    @abstractmethod
    def init_db(self) -> None:
        pass

    @abstractmethod
    def get_session(self) -> Generator[Any, None, None]:
        pass

    @abstractmethod
    def schema(self) -> str:
        pass

    @abstractmethod
    def all_records(self, model: Type[SQLModel]) -> List[SQLModel]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_record(
        self, model: Type[SQLModel], id: Any, alt_key: str = None
    ) -> Optional[SQLModel]:
        pass

    @abstractmethod
    def update_record(
        self, model: Type[SQLModel], id: Any, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_record(self, model: Type[SQLModel], id: Any) -> None:
        pass

    @abstractmethod
    def upsert_record(self, model: Type[SQLModel], data: Dict[str, Any]) -> SQLModel:
        pass

    @abstractmethod
    def bulk_insert(
        self, model: Type[SQLModel], data: List[Dict[str, Any]]
    ) -> List[SQLModel]:
        pass

    @abstractmethod
    def bulk_update(
        self, model: Type[SQLModel], data: List[Dict[str, Any]]
    ) -> List[SQLModel]:
        pass

    @abstractmethod
    def count_records(self, model: Type[SQLModel]) -> int:
        pass
