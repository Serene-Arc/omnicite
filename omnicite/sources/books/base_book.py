from abc import ABC
from typing import Optional

import confuse

from omnicite.sources.base_source import BaseSource


class BaseBook(BaseSource, ABC):
    entry_type = "book"
    required_fields = (
        "author",
        "title",
        [
            "year",
            "date",  # preferred
        ],
    )
    optional_fields = (
        "addendum",
        "afterword",
        "annotator",
        "chapter",
        "commentator",
        "doi",
        "edition",
        "editor",
        "editora",
        "editorb",
        "editorc",
        "eid",
        "eprint",
        "eprintclass",
        "eprinttype",
        "foreword",
        "introduction",
        "isbn",
        "language",
        "location",
        "mainsubtitle",
        "maintitle",
        "maintitleaddon",
        "note",
        "number",
        "origlanguage",
        "pages",
        "pagetotal",
        "part",
        "publisher",
        "pubstate",
        "series",
        "subtitle",
        "titleaddon",
        "translator",
        "url",
        "urldate",
        "volume",
        "volumes",
    )

    def __init__(self, identifier: str, configuration: Optional[confuse.Configuration]):
        super().__init__(identifier, configuration)
