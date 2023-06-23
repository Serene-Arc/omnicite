from abc import ABC
from typing import Iterator, Optional

import confuse

from omnicite.sources.base_source import BaseSource


class BaseArticle(BaseSource, ABC):
    entry_type = "article"
    required_fields = (
        "author",
        "journaltitle",
        "title",
        ["year", "date"],
    )
    optional_fields = (
        "addendum",
        "annotator",
        "commentator",
        "doi",
        "editor",
        "editora",
        "editorb",
        "editorc",
        "eid",
        "eprint",
        "eprintclass",
        "eprinttype",
        "issn",
        "issue",
        "issuesubtitle",
        "issuetitle",
        "issuetitleaddon",
        "journalsubtitle",
        "journaltitleaddon",
        "language",
        "month",
        "note",
        "number",
        "origlanguage",
        "pages",
        "pubstate",
        "series",
        "subtitle",
        "titleaddon",
        "translator",
        "url",
        "urldate",
        "version",
        "volume",
    )

    def __init__(self, identifier: str, configuration: Optional[confuse.Configuration]):
        super().__init__(identifier, configuration)

    def _unique_id_generator(self) -> Iterator[str]:
        essential_fields = (
            self.fields["author"].field_contents,
            self.fields["date"].year,
            self.fields["publication"],
        )
        yield from self._add_authors_id_generator(essential_fields)
        yield from self._increment_number_id_generator(essential_fields)
