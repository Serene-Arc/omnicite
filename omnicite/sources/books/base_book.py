from abc import ABC
from typing import Iterator, Optional

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

    def __init__(self, identifier: str):
        super().__init__(identifier)

    def _unique_id_generator(self) -> Iterator[str]:
        essential_fields = (
            self.fields["author"].field_contents,
            self.fields["date"].year,
        )
        yield from self._add_authors_id_generator(essential_fields)
        yield from self._increment_number_id_generator(essential_fields)
