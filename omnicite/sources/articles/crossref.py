from datetime import date

import crossref.restful

from omnicite.exceptions import OmniCiteSourceFieldError
from omnicite.sources.articles.base_article import BaseArticle
from omnicite.special_fields.date_field import DateField
from omnicite.special_fields.name_field import NameField


class Crossref(BaseArticle):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    async def retrieve_information(self, _):
        # TODO: make async
        work = crossref.restful.Works()
        work = work.doi(self.identifier)

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
            "urldate": DateField(date.today()),
        }
        if "page" in work:
            out["pages"] = work["page"]

        # flatten the dictionary in case any lists sneak in
        for key in out.keys():
            if isinstance(out[key], list):
                if len(out[key]) == 1:
                    out[key] = out[key][0]
                else:
                    raise OmniCiteSourceFieldError(f"Dictionary for key '{key}' is a list has {len(out[key])} values")
        self.fields = out
