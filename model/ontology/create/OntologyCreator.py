from owlready2 import Thing

from model.ontology.create.OntologyInstancesCreator import OntologyInstancesCreator


class OntologyCreator:
    """"
    Класс отвечающий за созадние онтологии.

    Получает на вход онтологию, значение префикса классов, которые будут добалвены в онтологию
    """

    def __init__(self, onto, classes_prefix=""):
        self.__onto = onto
        self.__created_classes_name_to_owl_classes = {}
        self.__classes_prefix = classes_prefix
        self.__instances_creator = OntologyInstancesCreator(self.__onto, self.__classes_prefix)

    def create_owl_instances(self, wiki_pages):
        self.__instances_creator.create_owl_instances(self.__created_classes_name_to_owl_classes, wiki_pages)

    # Метод создающий классы и складывающий их в хранилище ключ значение
    # :key - имя класса :value - класс
    def create_owl_classes(self, wiki_categories_pages_and_parents):
        for category_name, category_page_and_parents in wiki_categories_pages_and_parents.items():
            parents_classes_names = category_page_and_parents[1]

            if category_name in self.__created_classes_name_to_owl_classes:
                continue

            parents_classes = self.__get_classes(parents_classes_names, wiki_categories_pages_and_parents)

            if not parents_classes:
                self.__create_root_owl_class(category_name)
            else:
                self.__create_owl_class(category_name, parents_classes)

    # Создает класс онтологии - родитель owl.Thing
    def __create_root_owl_class(self, class_name):
        new_class = type(self.__classes_prefix + class_name, (Thing,), {'namespace': self.__onto})
        self.__put_class(new_class)
        return new_class

    # Создает класс онтологии, получает на вход название и список родитеских классов
    def __create_owl_class(self, class_name, parent_classes):
        new_class = type(self.__classes_prefix + class_name, tuple(parent_classes), {'namespace': self.__onto})
        self.__put_class(new_class)
        return new_class

    def __put_class(self, created_class):
        self.__created_classes_name_to_owl_classes[created_class.name] = created_class

    # Используется для получения классов по списку их названий
    def __get_classes(self, classes_names, wiki_categories_pages_and_parents):
        classes = []
        for class_name in classes_names:
            classes.append(self.__create_and_get_owl_class(class_name, wiki_categories_pages_and_parents))
        return classes

    # Используется для получения родительского класса
    # Если такого класса нет, то возвращает owl.Thing
    def __create_and_get_owl_class(self, class_name, wiki_categories_pages_and_parents):
        try:
            owl_class = self.__created_classes_name_to_owl_classes[class_name]
        except KeyError:
            owl_class = None

        if owl_class is not None:
            return owl_class

        # Smth class has category, but page was not created
        try:
            category_page_and_parents = wiki_categories_pages_and_parents[class_name]
        except KeyError:
            return Thing

        parent_classes = category_page_and_parents[1]
        if not parent_classes:
            return self.__create_root_owl_class(class_name)

        parent_owl_classes_to_create = []
        for parent_class in parent_classes:
            try:
                owl_class = self.__created_classes_name_to_owl_classes[parent_class]
            except KeyError:
                owl_class = None

            if owl_class is not None:
                parent_class_to_create = owl_class
            else:
                parent_class_to_create = self.__create_and_get_owl_class(parent_class,
                                                                         wiki_categories_pages_and_parents)

            parent_owl_classes_to_create.append(parent_class_to_create)

        return self.__create_owl_class(class_name, parent_owl_classes_to_create)
