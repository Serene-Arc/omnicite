from abc import ABC, abstractmethod
from typing import Type

from omnicite.sources.base_source import BaseSource


class BaseFactory(ABC):
    @classmethod
    @abstractmethod
    def pull_lever(cls, identifier: str) -> Type[BaseSource]:
        raise NotImplementedError
