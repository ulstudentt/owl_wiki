from model.wiki.create.CategoryCreator import CategoryCreator


class WikiCreator:
    """"
    Класс, извлекающий классы и передающий свойства
    непосредственно генератору wiki ресурса

    create_wiki_pages() - принимает онтологию, вызывает создание категорий wiki ресурса

    Конструктор принимает на вход свойства онтологии, максимальное количетсво
    объектов для одного класса, соединение
    """
    def __init__(self, onto_properties, max_page_for_category, wiki_connector):
        self.__ontoProperties = onto_properties
        self.connector = wiki_connector
        self.__site = self.connector.get_logged_site()
        self.__max_page_for_category = max_page_for_category

    def create_wiki_pages(self, onto):
        CategoryCreator(self.__site, self.__ontoProperties, onto, self.__max_page_for_category) \
            .create_categories(onto.classes())
