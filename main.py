from owlready2 import *

from model.ontology.OntologyParser import OntologyParser
from model.wiki.create.WikiCreator import WikiCreator

# onto = get_ontology("http://protege.stanford.edu/ontologies/pizza/pizza.owl")
onto = get_ontology("http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/job.owl")
# onto = get_ontology("http://files.ifi.uzh.ch/ddis/oldweb/ddis/fileadmin/ont/nli/restaurant.owl")
onto.load()

ontologyParser = OntologyParser()
ontoProperties = ontologyParser.get_properties(onto)

wikiCreator = WikiCreator(ontoProperties)

wikiCreator.create_wiki_pages(onto)

for page in site.pages:
    print("Wiki page:" + page.name)
"""
for owlClass in owlClasses:
    page = site.pages[owlClass.name]
    page.save("text","smthtext")
"""
page = site.pages["Category:testCategory"]
page.categories("testcategory1")
page.categories("testcategory2")
page.save("mytext", "smthtext")

secondPage = site.pages["Category: testCategory2"]
secondPage.save("[[Category:testCategory]]", "smthtext")

secondPage = site.pages["pageForTestCategory"]
secondPage.save("[[Category:testCategory]]", "smthtext")

a = 2
print(a)
