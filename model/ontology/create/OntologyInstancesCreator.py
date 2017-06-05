import re

from owlready2 import Thing

from model.ontology.create.ParsedPropertyModel import ParsedPropertyModel


class OntologyInstancesCreator:
    """"
    Класс отвечающий за создание классов, объектов и заполнения их свойств
    """
    __category_wiki_text = "Category:"
    __infobox_wiki_text = "{{Infobox"
    __label = "label"
    __data = "data"

    def __init__(self, onto, classes_prefix):
        self.__onto = onto
        self.__created_classes_name_to_owl_classes = {}
        self.__classes_prefix = classes_prefix

    def create_owl_instances(self, created_classes_name_to_owl_classes, wiki_pages):
        self.__wiki_pages = wiki_pages
        self.__created_classes_name_to_owl_classes = created_classes_name_to_owl_classes
        for wiki_page in wiki_pages:
            self.__get_category_names_from_page(wiki_page)

    # получает класс из словаря уже созданных классов,
    # создает  объект класса, после этого вызывает создание и заполнение свойств объекта
    def __get_category_names_from_page(self, wiki_page):
        text = wiki_page.text()
        search_res = re.findall('\[\[' + self.__category_wiki_text + '(.*?)\]\]', text)
        owl_class = None
        if search_res.__len__() > 0:  # TODO ONLY FOR ONE YET
            owl_class = self.__created_classes_name_to_owl_classes[self.__classes_prefix + search_res[0]]
            instance = self.__create_instance(owl_class, wiki_page.name)
        else:
            instance = self.__create_root_owl_class(wiki_page.name)
            # TODO PROPERTIES FROM instance-category
            return
        self.__add_properties_to_instance_and_class(instance, owl_class, wiki_page.text())

    def __put_class(self, created_class):
        self.__created_classes_name_to_owl_classes[created_class.name] = created_class

    # метод создания класса налседующегося от owl.Thing
    def __create_root_owl_class(self, class_name):
        new_class = type(self.__classes_prefix + class_name, (Thing,), {'namespace': self.__onto})
        self.__put_class(new_class)
        return new_class

    # метод создания свойства и доабвление его значения объекту
    def __add_properties_to_instance_and_class(self, instance, owl_class, page_text):
        if self.__infobox_wiki_text not in page_text:
            return

        parameter_number_with_model = {}
        search_res = re.search(self.__infobox_wiki_text + '(.*?)}}', page_text)
        if search_res is not None:
            res = search_res.regs[1]
            infobox_text = page_text[res[0] + 2:res[1]]
            parameters = infobox_text.split("|")
            for parameter in parameters:
                label_or_data = parameter.split("=")

                label_or_data[0] = label_or_data[0].strip()
                label_or_data[1] = label_or_data[1].strip()

                key = label_or_data[0][-1]
                if self.__label in label_or_data[0]:
                    self.__add_property_label(key, label_or_data[1], parameter_number_with_model)
                elif self.__data in label_or_data[0]:
                    self.__add_property_value(key,
                                              label_or_data[1],
                                              parameter_number_with_model,
                                              owl_class)

            for key, property_model in parameter_number_with_model.items():
                if property_model.get_is_class_property():
                    try:
                        property_model.create_property_class(self.__onto)
                    except TypeError:
                        print("Already created,think")
                    getattr(instance, property_model.get_label()).append(
                        property_model.create_instance_of_range_class())
                else:
                    try:
                        property_model.create_property_string(self.__onto)
                    except AttributeError:
                        print("Already created,think")
                    except TypeError:
                        print("Already created,think")
                    getattr(instance, property_model.get_label()).append(
                        property_model.get_value())

    # добавление в словарь свойств экземпляра значения свойства
    def __add_property_value(self, key, value, parameter_number_with_model, owl_class):
        property_model = ParsedPropertyModel()
        try:
            property_model = parameter_number_with_model[key]
        except KeyError:
            parameter_number_with_model[key] = ParsedPropertyModel()  # TODO not need

        search_res = re.search('\[\[(.*?)\]\]', value)
        if search_res is not None:
            res = search_res.regs[1]
            page_name = value[res[0]: res[1]]
            page = self.__get_page_by_name(page_name)
            if page is None:
                parameter_number_with_model[key].set_value(value)
                return
            property_class_range_name = self.__get_page_category(page)
            property_class_range = self.__created_classes_name_to_owl_classes[
                self.__classes_prefix + property_class_range_name]

            property_model.set_value(page_name)
            property_model.set_is_class_property(True)
            property_model.set_range(property_class_range)
            property_model.set_class_with_property(owl_class)

        else:
            property_model.set_value(value)
            property_model.set_class_with_property(owl_class)

        parameter_number_with_model[key] = property_model

    # добавление в словарь свойств экземпляра названия свойства
    def __add_property_label(self, key, label, parameter_number_with_model):
        try:
            parameter_number_with_model[key]
            parameter_number_with_model[key].set_label(label)
        except KeyError:
            propertyModel = ParsedPropertyModel()
            propertyModel.set_label(label)
            parameter_number_with_model[key] = propertyModel

    def __create_instance(self, parent_class, page_name):
        return parent_class(page_name)

    def __get_page_category(self, page):
        search_res = re.search("\[\[Category:" + '(.*?)\]\]', page.text())
        if search_res is not None:
            res = search_res.regs[1]
            category = page.text()[res[0]:res[1]]
            return category
        return None

    def __get_page_by_name(self, page_name):
        upper_page_name = page_name.upper()
        for page in self.__wiki_pages:
            if page.name.upper() == upper_page_name:
                return page
        return None
