import re
from datetime import date, datetime

import aiohttp
import bs4
import confuse

from omnicite.sources.websites.base_website import BaseWebsite
from omnicite.special_fields.date_field import DateField
from omnicite.special_fields.name_field import NameField


class Substack(BaseWebsite):
    def __init__(self, url: str):
        super().__init__(url)

    async def retrieve_information(self, configuration: confuse.Configuration):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.identifier) as resp:
                text = await resp.text()
        soup = bs4.BeautifulSoup(text)

        # Use the function as the argument to the find method
        post_date_elements = soup.find_all(
            "div", attrs={"class": re.compile(r"frontend-pencraft-Text-module__transform-uppercase")}
        )
        post_date = list(filter(lambda e: e.text and re.match(r"\b\w{3} \d{1,2}, \d{4}\b", e.text), post_date_elements))
        post_date = post_date[0].text

        subtitle = (
            soup.find("h3", attrs={"class": "subtitle"}).text if soup.find("h3", attrs={"class": "subtitle"}) else ""
        )
        self.fields = {
            "title": soup.find("h1", attrs={"class": "post-title"}).text.strip(),
            "author": NameField(
                soup.find(
                    "a", attrs={"class": "pencraft", "href": re.compile(r"https://substack.com/@.*")}
                ).text.strip()
            ),
            "date": DateField(datetime.strptime(post_date, "%b %d, %Y").date()),
            "organization": "Substack",
            "subtitle": subtitle.strip(),
            "url": self.identifier,
            "urldate": date.today(),
        }

    @property
    def website_citation_suffix(self) -> str:
        return "substack"
