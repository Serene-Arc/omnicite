from abc import ABC
from typing import Sequence

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

    def __init__(self, url: str):
        super().__init__(url)

    def generate_unique_identifier(self, existing_identifiers: Sequence[str]) -> str:
        pass
