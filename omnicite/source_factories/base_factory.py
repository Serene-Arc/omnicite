from abc import ABC, abstractmethod
from typing import Type

from omnicite.sources.base_source import BaseSource


class BaseFactory(ABC):
    @staticmethod
    @abstractmethod
    def pull_lever(identifier: str) -> Type[BaseSource]:
        raise NotImplementedError
