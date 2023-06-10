from abc import ABC, abstractmethod, abstractproperty
from typing import Iterator, Optional, Sequence

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
