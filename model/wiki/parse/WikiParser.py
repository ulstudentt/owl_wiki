import re

from model.ontology.create.OntologyCreator import OntologyCreator
from model.wiki.WikiConnector import WikiConnector


class WikiParser:
    category_text = "Category:"

    connector = WikiConnector()

    def __init__(self):
        self.site = self.connector.get_logged_site()

    def get_category_pages(self):
        categories_pages = self.site.categories
        category_pages_and_parents = {}
        for category_page in categories_pages:
            category_pages_and_parents[category_page.page_title] = (category_page,[])
            page_text = category_page.text()
            search_res = re.findall(r'\[\[(' + self.category_text + ')(.*?)]]', page_text)

            for occurrence in search_res:
                category_pages_and_parents[category_page.page_title][1].append(occurrence[1])
        return category_pages_and_parents


