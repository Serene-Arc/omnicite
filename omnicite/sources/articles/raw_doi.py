from typing import Sequence

from omnicite.sources.articles.base_article import BaseArticle


class RawDOI(BaseArticle):
    def __init__(self, identifier: str):
        super().__init__(identifier, None)

    def retrieve_information(self):
        self.fields = self.get_doi_information(self.identifier)
