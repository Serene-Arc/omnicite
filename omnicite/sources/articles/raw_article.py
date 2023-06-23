from omnicite.sources.articles.base_article import BaseArticle


class RawArticle(BaseArticle):
    def __init__(self, identifier: str):
        super().__init__(identifier, None)

    def retrieve_information(self):
        pass
