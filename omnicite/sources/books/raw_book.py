from omnicite.sources.books.base_book import BaseBook


class RawBook(BaseBook):
    def __init__(self, isbn: str):
        super().__init__(isbn)

    async def retrieve_information(self, _):
        pass
