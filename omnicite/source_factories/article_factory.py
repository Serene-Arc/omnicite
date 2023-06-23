from typing import Type

from omnicite.source_factories.base_factory import BaseFactory
from omnicite.sources.articles.crossref import Crossref
from omnicite.sources.base_source import BaseSource


class ArticleFactory(BaseFactory):
    @staticmethod
    def pull_lever(identifier: str) -> Type[BaseSource]:
        return Crossref
