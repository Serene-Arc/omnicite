import json
from typing import Iterator

import isbnlib

from omnicite.exceptions import OmniCiteSourceException
from omnicite.sources.books.base_book import BaseBook
from omnicite.special_fields.name_field import NameField


class ISBNLib(BaseBook):
    def __init__(self, isbn: str):
        super().__init__(isbn)

    async def retrieve_information(self, _):
        if isbnlib.notisbn(self.identifier):
            raise OmniCiteSourceException(f"String '{self.identifier}' is not a valid ISBN")
        book_info = isbnlib.meta(self.identifier, service="default")

        self.fields = {
            "doi": isbnlib.doi(self.identifier),
            "author": NameField(book_info["Authors"]),
            "title": book_info["Title"],
            "publisher": book_info["Publisher"],
            "year": book_info["Year"],
            "isbn": book_info["ISBN-13"],
        }
