import types

from owlready2 import Thing


class OntologyCreator:
    def __init__(self, onto, classes_prefix=""):
        self.onto = onto
        self.created_classes_name_to_owl_classes = {}
        self.classes_prefix = classes_prefix

    def create_owl_classes(self, wiki_categories_pages_and_parents):
        for category_name, category_page_and_parents in wiki_categories_pages_and_parents.items():
            parents_classes_names = category_page_and_parents[1]

            if category_name in self.created_classes_name_to_owl_classes:
                continue

            parents_classes = self.__get_classes(parents_classes_names, wiki_categories_pages_and_parents)

            if not parents_classes:
                self.__create_root_owl_class(category_name)
            else:
                self.__create_owl_class(category_name, parents_classes)

        self.onto.save("myowl.owl", format="rdfxml")

    def __create_root_owl_class(self, class_name):
        new_class = type(self.classes_prefix + class_name, (Thing,), {'namespace': self.onto})
        self.__put_class(new_class)
        return new_class

    def __create_owl_class(self, class_name, parent_classes):
        new_class = type(self.classes_prefix + class_name, tuple(parent_classes), {'namespace': self.onto})
        self.__put_class(new_class)
        return new_class

    def __put_class(self, created_class):
        self.created_classes_name_to_owl_classes[created_class.name] = created_class

    def __get_classes(self, classes_names, wiki_categories_pages_and_parents):
        classes = []
        for class_name in classes_names:
            classes.append(self.__create_and_get_owl_class(class_name, wiki_categories_pages_and_parents))
        return classes

    def __create_and_get_owl_class(self, class_name, wiki_categories_pages_and_parents):
        try:
            owl_class = self.created_classes_name_to_owl_classes[class_name]
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
                owl_class = self.created_classes_name_to_owl_classes[parent_class]
            except KeyError:
                owl_class = None

            if owl_class is not None:
                parent_class_to_create = owl_class
            else:
                parent_class_to_create = self.__create_and_get_owl_class(parent_class,
                                                                         wiki_categories_pages_and_parents)

            parent_owl_classes_to_create.append(parent_class_to_create)

        return self.__create_owl_class(class_name, parent_owl_classes_to_create)
