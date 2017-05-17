from mwtemplates import TemplateEditor


class PagesCreator:
    def __init__(self, wiki_site, properties, onto):
        self.__site = wiki_site
        self.properties = properties
        self.__onto = onto

    def create_pages(self, instances):
        for instance in instances:
            self.__create_page(instance)

    def __create_page(self, instance):
        page = self.__site.pages[instance.name]
        self.__add_page_to_categories(page, instance)
        if not page.exists:
            page.save(page.text())

    def __add_page_to_categories(self, page, instance):
        was_changed = False
        text = page.text()
        for parent in instance.is_a:
            if parent.name not in page.text():
                text += "[[Category:" + parent.name + "]]"
                was_changed = True

        self.__add_infoblock_to_page(page, instance)
        if was_changed:
            page.save(text)

    def __add_infoblock_to_page(self, page, instance):
        all_classes_for_properties = self.__get_all_parents_names(instance)

        templates = TemplateEditor(page.text())
        infobox = templates['Infobox']
        """for class_name_for_property in all_classes_for_properties:
            if parent.name in self.properties:
                templates = TemplateEditor(page.text())"""
        infobox = templates['Infobox']
        # for property in self.properties[parent.name]:

    def __get_all_parents_names(self, instance):
        parent_classes_names = []

        for parent_class in instance.is_a:
            parent_classes_names.append(parent_class.name)
            parent_classes_names += self.__get_parents_for_class(parent_class)

        return parent_classes_names

    def __get_parents_for_class(self, owl_class):
        parent_classes_names = []
        for parent in owl_class.is_a:
            if (parent.name != "Thing") | (parent.name != "DomainConcept"):
                parent_classes_names.append(parent.name)
                for parent_class in parent.is_a:
                    parent_classes_names += self.__get_parents_for_class(parent_class)
        return parent_classes_names
