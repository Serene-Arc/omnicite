from typing import Sequence

from omnicite.sources.articles.base_article import BaseArticle


class RawDOI(BaseArticle):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    def generate_unique_identifier(self, existing_identifiers: Sequence[str]) -> str:
        # TODO
        raise NotImplementedError

    def retrieve_information(self):
        self.fields = self.get_doi_information(self.identifier)
