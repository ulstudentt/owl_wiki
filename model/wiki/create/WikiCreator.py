from mwtemplates import TemplateEditor

from model.wiki.WikiConnector import WikiConnector
from model.wiki.create.CategoryCreator import CategoryCreator
from model.wiki.create.PagesCreator import PagesCreator


class WikiCreator:
    connector = WikiConnector()

    def __init__(self, onto_properties):
        self.ontoProperties = onto_properties
        self.site = self.connector.get_logged_site()

    def create_wiki_pages(self, onto):
        CategoryCreator(self.site, self.ontoProperties, onto).create_categories(onto.classes())
