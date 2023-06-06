from typing import Type
from urllib.parse import ParseResult, urlparse

from omnicite.source_factories.base_factory import BaseFactory
from omnicite.sources.base_source import BaseSource
from omnicite.sources.websites.new_york_times_website import NewYorkTimesWebsite


class WebsiteFactory(BaseFactory):
    @staticmethod
    def pull_lever(identifier: str) -> Type[BaseSource]:
        url_parts = WebsiteFactory.split_url(identifier)
        if "nytimes.com" in url_parts.netloc:
            return NewYorkTimesWebsite

    @staticmethod
    def split_url(identifier: str) -> ParseResult:
        return urlparse(identifier)
