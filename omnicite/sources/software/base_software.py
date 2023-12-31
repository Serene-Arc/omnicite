from abc import ABC

import confuse

from omnicite.sources.base_source import BaseSource


class BaseSoftware(BaseSource, ABC):
    entry_type = "software"
    required_fields = (
        "title",
        [
            "author",
            "editor",
        ],
        [
            "date",
            "year",
        ],
    )
    optional_fields = (
        "addendum",
        "doi",
        "eprint",
        "eprintclass",
        "eprinttype",
        "howpublished",
        "language",
        "location",
        "month",
        "note",
        "organization",
        "pubstate",
        "subtitle",
        "titeladdon",
        "type",
        "url",
        "urldate",
        "version",
    )

    def __init__(self, identifier: str):
        super().__init__(identifier)
