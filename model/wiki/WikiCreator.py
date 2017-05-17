from mwtemplates import TemplateEditor

from model.wiki.WikiConnector import WikiConnector


class WikiCreator:
    connector = WikiConnector()

    def __init__(self):
        self.site = self.connector.get_logged_site()

    def create_wiki_pages(self, owl_classes):
        for owl_class in owl_classes:
            self.create_category(owl_class.name)
            if not self.is_root_element(owl_class):
                self.add_class_in_parent_categories(owl_class)

    def create_category(self, category_name):
        page = self.site.pages["Category:" + category_name]
        page.save(page.text())

    def add_class_in_parent_categories(self, owl_class):
        page = self.site.pages["Category:" + owl_class.name]
        for parent_category in owl_class.is_a:
            page.save(page.text() + "[[Category:" + parent_category.name + "]]")

    # check if is_a field foreach need
    def is_root_element(self, owl_class):
        parent_name = owl_class.is_a[0].name;
        if (parent_name == "Thing") | (parent_name == "DomainConcept"):
            return True
        else:
            return False

    def is_root_category(self,category_name):
        if (category_name == "Thing") | (category_name == "DomainConcept"):
            return True
        else:
            return False