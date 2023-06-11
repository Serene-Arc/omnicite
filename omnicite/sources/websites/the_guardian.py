import json
import re
from datetime import date, datetime
from typing import Sequence

import bs4
import confuse
import requests

from omnicite.exceptions import OmniCiteSourceException
from omnicite.sources.websites.base_website import BaseWebsite
from omnicite.special_fields.date_field import DateField
from omnicite.special_fields.name_field import NameField


class TheGuardian(BaseWebsite):
    def __init__(self, url: str, configuration: confuse.Configuration):
        super().__init__(url, configuration)

    @property
    def website_citation_suffix(self) -> str:
        return "guardian"

    def retrieve_information(self):
        api_url = re.sub(r"(www\.)?theguardian\.com", "content.guardianapis.com", self.identifier)
        response = requests.get(
            api_url,
            params={
                "api-key": self.configuration["apis"]["the_guardian"]["api_key"].get(),
                "show-fields": "all",
            },
        )
        data = json.loads(response.text)
        if data["response"]["total"] != 1:
            raise OmniCiteSourceException(f"Call to The Guardian API returned {data['response']['total']} results")
        data = data["response"]["content"]
        date_text = (
            data["fields"]["newspaperEditionDate"]
            if "newspaperEditionDate" in data["fields"]
            else data["fields"]["firstPublicationDate"]
        )
        self.fields = {
            "title": data["fields"]["headline"],
            "subtitle": data["fields"]["trailText"],
            "url": data["webUrl"],
            "urldate": DateField(date.today()),
            "organization": data["fields"]["publication"],
            "date": DateField(datetime.fromisoformat(date_text).date()),
            "author": NameField(self._parse_html_byline(data["fields"]["bylineHtml"])),
        }

    @staticmethod
    def _parse_html_byline(byline: str) -> Sequence[str]:
        soup = bs4.BeautifulSoup(byline)
        links = soup.find_all("a")
        out = [link.text for link in links]
        return out
