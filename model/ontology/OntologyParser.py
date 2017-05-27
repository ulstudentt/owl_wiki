class OntologyParser:
    def get_properties(self, onto):
        classes_to_properties = {}

        onto.properties()
        self.__parse_properties_list(classes_to_properties, onto.properties())
        self.__parse_properties_list(classes_to_properties, onto.data_properties())
        self.__parse_properties_list(classes_to_properties, onto.annotation_properties())
        return classes_to_properties

    @staticmethod
    def __parse_properties_list(classes_to_properties, properties):
        for property in properties:
            classAndPropertyNames = str(property).split('.')
            className = classAndPropertyNames[0].lower()
            propertyName = classAndPropertyNames[1]
            if classes_to_properties.get(className) is None:
                classes_to_properties[className] = []
            classes_to_properties[className].append(propertyName)
