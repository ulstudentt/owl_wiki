from owlready2 import ObjectProperty, DataProperty, Thing


class ParsedPropertyModel:
    def __init__(self, label=None, value=None, is_class_property=False, range=None, class_with_property=None):
        self.__label = label
        self.__value = value
        self.__is_class_property = is_class_property
        self.__range = range
        self.__class_with_property = class_with_property

    def set_label(self, label):
        self.__label = label

    def get_label(self):
        return self.__label

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def set_is_class_property(self, is_class_property):
        self.__is_class_property = is_class_property

    def get_is_class_property(self):
        return self.__is_class_property

    def set_range(self, range):
        self.__range = range

    def get_range(self):
        return self.__range

    def set_class_with_property(self, class_with_property):
        self.__class_with_property = class_with_property

    def get_class_with_property(self):
        return self.__class_with_property

    def create_property_class(self, onto):
        return type(self.get_label(), (ObjectProperty,),
                    {'namespace': onto, 'range': [self.get_range()], 'domain': [self.get_class_with_property()]})

    def create_property_string(self, onto):
        if self.get_class_with_property() is Thing:
            a = 2
        return type(self.get_label(), (DataProperty,),
                    {'namespace': onto, 'range': [str], 'domain': [self.get_class_with_property()]})

    def create_instance_of_range_class(self):
        range_class = self.get_range()
        return range_class(self.get_label())
