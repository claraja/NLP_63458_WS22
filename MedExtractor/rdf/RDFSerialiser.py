from interfaces.interfaces import RDFSerialiserInterface
from rdflib import Graph, Literal, Namespace
from rdflib.term import URIRef
from graphmanager import GraphManager

class RDFSerialiser(RDFSerialiserInterface):
    def serialise_knowledgebase(self):
        graph = GraphManager("fapra", "http://fapranlp.de/")
        graph.add_disease("depression")
        graph.add_symptom("depression", "lack of motivation")
        graph.add_symptom("depression", "sadness")

        return graph.get_serialised_graph()
#%%
