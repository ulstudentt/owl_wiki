from owlready2 import *

from model.ontology.OntologyParser import OntologyParser
from model.ontology.create.OntologyCreator import OntologyCreator
from model.wiki.create.WikiCreator import WikiCreator
from model.wiki.parse.WikiParser import WikiParser

# onto = get_ontology("http://protege.stanford.edu/ontologies/pizza/pizza.owl")
# onto = get_ontology("http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/job.owl")
# onto = get_ontology("http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/restaurant.owl")

create = False

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
    wikiCreator = WikiCreator(ontoProperties)
    wikiCreator.create_wiki_pages(onto)
    sys.exit("Successful")
else:
    path = "http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/job.owl"
    onto = create_ontology(path)
    wikiParser = WikiParser()
    ontologyCreator = OntologyCreator(onto,"My")
    ontologyCreator.create_owl_classes(wikiParser.get_category_pages())
