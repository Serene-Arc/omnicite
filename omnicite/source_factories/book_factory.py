from typing import Type

from omnicite.source_factories.base_factory import BaseFactory
from omnicite.sources.base_source import BaseSource
from omnicite.sources.books.raw_isbn import RawISBN


class BookFactory(BaseFactory):
    @staticmethod
    def pull_lever(identifier: str) -> Type[BaseSource]:
        return RawISBN