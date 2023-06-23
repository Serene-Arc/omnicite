from abc import ABC, abstractmethod
from typing import Iterator, Optional

import confuse

from omnicite.sources.base_source import BaseSource


class BaseWebsite(BaseSource, ABC):
    """Equivalent to the 'online' bibtex source."""

    entry_type = "online"
    required_fields = [
        "title",
        [
            "author",  # preferred
            "editor",
        ],
        [
            "date",  # preferred
            "year",
        ],
        [
            "doi",
            "eprint",
            "url",  # preferred
        ],
    ]
    optional_fields = [
        "addendum",
        "eprintclass",
        "eprinttype",
        "language",
        "month",
        "note",
        "organization",
        "pubstate",
        "subtitle",
        "titeladdon",
        "urldate",
        "version",
    ]

    def __init__(self, url: str, configuration: Optional[confuse.Configuration]):
        super().__init__(url, configuration)

    @property
    @abstractmethod
    def website_citation_suffix(self) -> str:
        raise NotImplementedError

    def _unique_id_generator(self) -> Iterator[str]:
        essential_fields = (
            self.fields["author"].field_contents,
            self.fields["date"].year,
            self.website_citation_suffix,
        )
        yield from self._add_authors_id_generator(essential_fields)
        yield from self._increment_number_id_generator(essential_fields)
