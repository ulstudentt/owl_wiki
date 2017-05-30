from model.wiki.create.PagesCreator import PagesCreator


class CategoryCreator:
    def __init__(self, wiki_site, properties, onto):
        self.__site = wiki_site
        self.__pages_creator = PagesCreator(self.__site, properties, onto)

    def create_categories(self, owl_classes):
        for owl_class in owl_classes:
            if owl_class.name == 'ITJob': #TODO убрать
                self.__create_category(owl_class.name)

                if not self.__is_root_category(owl_class):
                    self.__add_class_in_parent_categories(owl_class)

                self.__pages_creator.create_pages(owl_class.instances())

    def __create_category(self, category_name):
        category = self.__site.pages["Category:" + category_name]
        if not category.exists:
            category.save(category.text())

    def __add_class_in_parent_categories(self, owl_class):
        category = self.__site.pages["Category:" + owl_class.name]
        for parent_category in owl_class.is_a:
            if parent_category.name not in category.text():
                category.save(category.text() + "[[Category:" + parent_category.name + "]]")

    # check if is_a field foreach need
    def __is_root_category(self, owl_class):
        category_name = owl_class.is_a[0].name
        if (category_name == "Thing") | (category_name == "DomainConcept"):
            return True
        else:
            return False
