from typing import Type
from urllib.parse import ParseResult, urlparse

import bs4
import requests

from omnicite.source_factories.base_factory import BaseFactory
from omnicite.sources.base_source import BaseSource
from omnicite.sources.websites.new_york_times import NewYorkTimes
from omnicite.sources.websites.substack import Substack
from omnicite.sources.websites.the_guardian import TheGuardian


class WebsiteFactory(BaseFactory):
    @staticmethod
    def pull_lever(identifier: str, _) -> Type[BaseSource]:
        # try to match off first by the URL itself without making any web requests.
        url_parts = WebsiteFactory.split_url(identifier)
        if "nytimes.com" in url_parts.netloc:
            return NewYorkTimes
        elif "theguardian.com" in url_parts.netloc:
            return TheGuardian

        # sites below here require parsing the webpage to determine the class.
        page = requests.get(identifier)
        soup = bs4.BeautifulSoup(page.text)
        if WebsiteFactory.is_substack_page(soup):
            return Substack

    @staticmethod
    def is_substack_page(soup: bs4.BeautifulSoup) -> bool:
        footer = soup.find("div", attrs={"class": "footer-slogan-blurb"})
        result = footer is not None and "Substack\xa0is the home for great writing" in footer.text
        return result

    @staticmethod
    def split_url(identifier: str) -> ParseResult:
        return urlparse(identifier)
