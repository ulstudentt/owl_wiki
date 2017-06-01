from model.wiki.WikiConnector import WikiConnector
from model.wiki.create.CategoryCreator import CategoryCreator


class WikiCreator:
    connector = WikiConnector()

    def __init__(self, onto_properties, max_page_for_category):
        self.__ontoProperties = onto_properties
        self.__site = self.connector.get_logged_site()
        self.__max_page_for_category = max_page_for_category

    def create_wiki_pages(self, onto):
        CategoryCreator(self.__site, self.__ontoProperties, onto, self.__max_page_for_category)\
            .create_categories(onto.classes())
