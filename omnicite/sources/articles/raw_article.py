from omnicite.sources.articles.base_article import BaseArticle


class RawArticle(BaseArticle):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    async def retrieve_information(self, _):
        pass
