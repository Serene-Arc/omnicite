from abc import ABC, abstractmethod
from typing import Optional, Type

import confuse

from omnicite.sources.base_source import BaseSource


class BaseFactory(ABC):
    @staticmethod
    @abstractmethod
    def pull_lever(identifier: str, configuration: Optional[confuse.Configuration] = None) -> Type[BaseSource]:
        raise NotImplementedError
