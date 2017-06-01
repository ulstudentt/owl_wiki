import argparse

from owlready2 import *

from model.ontology.OntologyParser import OntologyParser
from model.ontology.create.OntologyCreator import OntologyCreator
from model.wiki.WikiConnector import WikiConnector
from model.wiki.create.WikiCreator import WikiCreator
from model.wiki.parse.WikiParser import WikiParser


def take_param_val(str):
    return str.split('=')[1]


# onto = get_ontology("http://protege.stanford.edu/ontologies/pizza/pizza.owl")
# onto = get_ontology("http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/job.owl")
# onto = get_ontology("http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/restaurant.owl")
print("Работа началась")
parser = argparse.ArgumentParser(description='Taking parameters')
parser.add_argument('create')
parser.add_argument('login')
parser.add_argument('password')
parser.add_argument('ex_owl')
parser.add_argument('dest_owl')
parser.add_argument('server')
parser.add_argument('postfix')
args = parser.parse_args()
print("Аргументы получены")
create = take_param_val(args.create.upper())
max_count_pages_for_category = 100


def create_ontology(path):
    try:
        onto = get_ontology(path)
        onto.load()
        return onto
    except Exception:
        sys.exit("Error loading")


wikiConnector = WikiConnector(take_param_val(args.login),
                              take_param_val(args.password),
                              take_param_val(args.server),
                              take_param_val(args.postfix))

if create == 'TRUE':
    # "http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/job.owl"
    print("Создание wiki")
    path = take_param_val(args.ex_owl)
    onto = create_ontology(path)
    ontologyParser = OntologyParser()
    ontoProperties = ontologyParser.get_properties(onto)
    wikiCreator = WikiCreator(ontoProperties, max_count_pages_for_category, wikiConnector)
    wikiCreator.create_wiki_pages(onto)
    sys.exit("Generating successful")
elif create == 'FALSE':
    print("Создание онтологии началось")
    onto = create_ontology("http://localhost/root-ontology.owl")
    wikiParser = WikiParser(wikiConnector)
    ontologyCreator = OntologyCreator(onto, "My")
    ontologyCreator.create_owl_classes(wikiParser.get_category_pages())
    ontologyCreator.create_owl_instances(list(wikiParser.get_instance_pages()))
    # myowl.owl
    onto.save(take_param_val(args.dest_owl), format="rdfxml")
    sys.exit("Creating owl successful")
