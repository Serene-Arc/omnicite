import re
from typing import Type

import confuse
import isbnlib
import validators

from omnicite.exceptions import OmniCiteException
from omnicite.source_factories.article_factory import ArticleFactory
from omnicite.source_factories.base_factory import BaseFactory
from omnicite.source_factories.book_factory import BookFactory
from omnicite.source_factories.website_factory import WebsiteFactory
from omnicite.sources.articles.crossref import Crossref
from omnicite.sources.base_source import BaseSource
from omnicite.sources.books.isbnlib import ISBNLib
from omnicite.sources.software.github_repository import GitHubRepository
from omnicite.sources.websites.new_york_times import NewYorkTimes
from omnicite.sources.websites.the_guardian import TheGuardian

master_source_list = {
    "ISBNlib": ISBNLib,
    "Crossref": Crossref,
    "New York Times": NewYorkTimes,
    "The Guardian": TheGuardian,
    "GitHub Repository": GitHubRepository,
}


class MainFactory(BaseFactory):
    @staticmethod
    def pull_lever(identifier: str, configuration: confuse.Configuration) -> Type[BaseSource]:
        if MainFactory.is_doi(identifier):
            return ArticleFactory.pull_lever(identifier, configuration)
        elif not isbnlib.notisbn(identifier):
            return BookFactory.pull_lever(identifier, configuration)
        elif MainFactory.is_url(identifier):
            return WebsiteFactory.pull_lever(identifier, configuration)
        raise OmniCiteException(f"Could not find a source type for identifier '{identifier}'")

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
