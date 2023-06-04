from abc import ABC, abstractmethod
from typing import Any


class BaseSpecialField(ABC):
    def __init__(self, field_contents: Any):
        self.field_contents = field_contents

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError
