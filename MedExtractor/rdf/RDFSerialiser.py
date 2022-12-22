from interfaces.interfaces import RDFSerialiserInterface
from rdflib import Graph, Literal, Namespace
from rdflib.term import URIRef
from graphmanager import GraphManager

class RDFSerialiser(RDFSerialiserInterface):
    #def serialise_knowledgebase(self):
    #    graph = GraphManager("fapra", "http://fapranlp.de/")
    #    graph.add_disease("depression")
    #    graph.add_symptom("depression", "lack_of_motivation")
    #    graph.add_symptom("depression", "sadness")
    #    return graph.get_serialised_graph()

    def knowledgebase_to_graph(self, knowledgebase, graph):
        #raise NotImplementedError
        graph.add_disease("depression")
        graph.add_symptom("depression", "lack_of_motivation")
        graph.add_symptom("depression", "sadness")
        return  graph

    def create_graph(self):
        return GraphManager(self.namespace_prefix, self.namespace)
#%%
