from abc import ABC, abstractmethod
from typing import Type

from omnicite.sources.base_source import BaseSource


class BaseFormatter(ABC):
    @staticmethod
    @abstractmethod
    def convert_source(
        source: BaseSource,
    ):
        raise NotImplementedError
