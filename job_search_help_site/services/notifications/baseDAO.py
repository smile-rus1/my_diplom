import abc
from typing import Iterable, Any


class BaseDAO(abc.ABC):
    def _orm_to_entity(self, orm: Any):
        ...

    def fetch_all(self) -> Iterable[Any]:
        ...

    def create_model(self, **data: Any):
        ...

    def fetch_one_from_model(self, model, **data) -> Any:
        return model.objects.filter(**data).first()
