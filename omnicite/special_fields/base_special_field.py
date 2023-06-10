from abc import ABC, abstractmethod
from typing import Any


class BaseSpecialField(ABC):
    def __init__(self, field_contents: Any):
        self.raw_field_contents = field_contents
        self.field_contents = self._construct_field()

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _construct_field(self) -> Any:
        raise NotImplementedError
