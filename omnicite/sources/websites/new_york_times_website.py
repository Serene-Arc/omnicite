import re
from datetime import date
from typing import Iterator, Sequence

import confuse
from pynytimes import NYTAPI

from omnicite.exceptions import OmniCiteSourceException
from omnicite.sources.websites.base_website import BaseWebsite
from omnicite.special_fields.date_field import DateField
from omnicite.special_fields.name_field import NameField


class NewYorkTimesWebsite(BaseWebsite):
    def __init__(self, url: str, configuration: confuse.Configuration):
        super().__init__(url, configuration)

    @staticmethod
    def split_and_sanitise_byline(in_string: str) -> Sequence[str]:
        in_string = in_string.lower()
        in_string = re.sub(r"^by ", "", in_string)
        out = re.split(r"( and )|(, )", in_string)
        out = [o.strip() for o in out if o]
        out = list(filter(lambda t: t not in ("", "and", ",", None), out))
        return out

    def retrieve_information(self):
        api_key = self.configuration["apis"]["new_york_times"]["api_key"].get()
        with NYTAPI(api_key, parse_dates=True) as nyt:
            article_metadata = nyt.article_metadata(self.identifier)
        if len(article_metadata) == 0:
            raise OmniCiteSourceException(f"URL '{self.identifier}' returned no matches from The New York Times API")
        elif len(article_metadata) > 1:
            raise OmniCiteSourceException(
                f"URL '{self.identifier}' returned {len(article_metadata)} " f"matches from The New York Times API"
            )
        article_metadata = article_metadata[0]

        self.fields = {
            "date": DateField(article_metadata["published_date"].date()),
            "organization": article_metadata["source"],
            "title": article_metadata["title"],
            "url": article_metadata["url"],
            "urldate": DateField(date.today()),
            "author": NameField.construct_name_field(self.split_and_sanitise_byline(article_metadata["byline"])),
            "subtitle": article_metadata["abstract"],
        }

    def _unique_id_generator(self) -> Iterator[str]:
        essential_fields = (
            self.fields["author"].field_contents,
            self.fields["date"].field_contents.year,
            "nyt",
        )
        for i in range(1, len(essential_fields[0]) + 1):
            yield BaseWebsite._format_unique_identifier(
                *[t.family_name for t in essential_fields[0][:i]],
                essential_fields[1],
                essential_fields[2],
            )

        i = 1
        while True:
            yield BaseWebsite._format_unique_identifier(
                *[t.family_name for t in essential_fields[0]],
                essential_fields[1],
                essential_fields[2],
                i,
            )
            i += 1