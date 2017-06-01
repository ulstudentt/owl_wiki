from model.wiki.create.CategoryCreator import CategoryCreator


class WikiCreator:
    def __init__(self, onto_properties, max_page_for_category, wiki_connector):
        self.__ontoProperties = onto_properties
        self.__site = self.connector.get_logged_site()
        self.__max_page_for_category = max_page_for_category
        self.connector = wiki_connector

    def create_wiki_pages(self, onto):
        CategoryCreator(self.__site, self.__ontoProperties, onto, self.__max_page_for_category) \
            .create_categories(onto.classes())
