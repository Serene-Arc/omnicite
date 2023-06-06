from abc import ABC
from typing import Sequence

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

    def __init__(self, url: str, configuration: confuse.Configuration = None):
        super().__init__(url, configuration)
