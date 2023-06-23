from abc import ABC
from typing import Optional

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
