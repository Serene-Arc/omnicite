import json
from abc import ABC

import crossref.restful

from omnicite.exceptions import OmniCiteSourceFieldError
from omnicite.sources.base_source import BaseSource
from omnicite.special_fields.base_special_field import BaseSpecialField
from omnicite.special_fields.date_field import DateField
from omnicite.special_fields.name_field import NameField


class BaseArticle(BaseSource, ABC):
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

    def __init__(self, identifier: str):
        super().__init__(identifier)

    @staticmethod
    def get_doi_information(doi: str) -> dict[str, str | BaseSpecialField]:
        work = crossref.restful.Works()
        work = work.doi(doi)

        out = {
            # required fields
            "author": NameField([f["given"] + " " + f["family"] for f in work["author"]]),
            "journaltitle": work["container-title"],
            "title": work["title"],
            "year": work["issued"]["date-parts"][0][0],
            # optional fields
            "doi": work["DOI"],
            "issn": work["ISSN"][0],
            "number": work["issue"],
            "month": work["issued"]["date-parts"][0][1],
            "publisher": work["publisher"],
            "url": work["URL"],
            "volume": work["volume"],
            "pages": work["page"],
        }

        # flatten the dictionary in case any lists sneak in
        for key in out.keys():
            if isinstance(out[key], list):
                if len(out[key]) == 1:
                    out[key] = out[key][0]
                else:
                    raise OmniCiteSourceFieldError(f"Dictionary for key '{key}' is a list has {len(out[key])} values")
        return out
