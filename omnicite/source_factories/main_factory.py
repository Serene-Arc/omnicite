import re
from typing import Type

import validators

from omnicite.source_factories.article_factory import ArticleFactory
from omnicite.source_factories.base_factory import BaseFactory
from omnicite.source_factories.website_factory import WebsiteFactory
from omnicite.sources.base_source import BaseSource


class MainFactory(BaseFactory):
    @staticmethod
    def pull_lever(identifier: str) -> Type[BaseSource]:
        if MainFactory.is_doi(identifier):
            return ArticleFactory.pull_lever(identifier)
        if MainFactory.is_url(identifier):
            return WebsiteFactory.pull_lever(identifier)

    @staticmethod
    def is_url(identifier: str) -> bool:
        if not identifier.startswith("http"):
            identifier = "http://" + identifier
        out = validators.url(identifier)
        return out if out is True else False

    @staticmethod
    def is_doi(identifier: str) -> bool:
        pattern = re.compile(r"^(https?://(doi\.org|dx\.doi\.org)/)?10.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)
        return bool(pattern.match(identifier))
