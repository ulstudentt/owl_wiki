from mwtemplates import TemplateEditor
import re


class PagesCreator:
    infobox_text = "Infobox"
    infobox_template_text = "{{Infobox }}"

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
        text = page.text()
        for parent in instance.is_a:
            parent_category_text = "[[Category:" + parent.name + "]]"
            if parent_category_text not in page.text():
                text += parent_category_text

        text = self.__get_text_with_infoblock(page.text(), instance)
        page.save(text)

    def __get_text_with_infoblock(self, text, instance):
        all_classes_for_properties = self.__get_all_parents_names(instance)
        properties = []
        for class_name in all_classes_for_properties:
            if class_name.lower() in self.properties:
                for property in self.properties[class_name.lower()]:
                    properties.append(property)

        template_editor = TemplateEditor(text)
        templatesFromText = template_editor
        if self.infobox_text in templatesFromText.templates:
            infobox = templatesFromText[self.infobox_text][0]
        else:
            template_editor = TemplateEditor(self.infobox_template_text)
            infobox = template_editor.templates[self.infobox_text][0]

        property_order = 0
        for property in properties:
            property_values = getattr(instance, property)

            try:
                property_values._Prop._range[0]._name
                property_with_class_value = True
            except AttributeError:
                property_with_class_value = False

            for property_value in property_values:
                property_order += 1

                if property_with_class_value:
                    property_value = property_value.name

                infobox.parameters['label{0}'.format(property_order)] = property
                infobox.parameters['data{0}'.format(property_order)] = \
                    '[[{0}]]'.format(str(property_value)) if property_with_class_value else str(property_value)

        search_res = re.search('{{(' + self.infobox_text + ')(.*?)}}', text)
        if search_res is not None:
            tuple_res = search_res.regs[0]
            text = re.sub(text[tuple_res[0]:tuple_res[1]], ' ', text)
        return template_editor.wikitext() + text

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
