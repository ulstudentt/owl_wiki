from owlready2 import *

from model.ontology.OntologyParser import OntologyParser
from model.ontology.create.OntologyCreator import OntologyCreator
from model.wiki.create.WikiCreator import WikiCreator
from model.wiki.parse.WikiParser import WikiParser

# onto = get_ontology("http://protege.stanford.edu/ontologies/pizza/pizza.owl")
# onto = get_ontology("http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/job.owl")
# onto = get_ontology("http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/restaurant.owl")

create = False
max_count_pages_for_category = 100


def create_ontology(path):
    try:
        onto = get_ontology(path)
        onto.load()
        return onto
    except Exception:
        sys.exit("Error loading")


if create:
    path = "http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/job.owl"
    onto = create_ontology(path)
    ontologyParser = OntologyParser()
    ontoProperties = ontologyParser.get_properties(onto)
    wikiCreator = WikiCreator(ontoProperties, max_count_pages_for_category)
    wikiCreator.create_wiki_pages(onto)
    sys.exit("Generating successful")
else:
    onto = create_ontology("http://localhost/root-ontology.owl")
    wikiParser = WikiParser()
    ontologyCreator = OntologyCreator(onto, "My")
    ontologyCreator.create_owl_classes(wikiParser.get_category_pages())
    ontologyCreator.create_owl_instances(list(wikiParser.get_instance_pages()))
    onto.save("myowl.owl", format="rdfxml")
    sys.exit("Creating owl successful")
