from rdflib import Graph, Literal,Namespace
from rdflib.term import URIRef


class GraphManager:
    def __init__(self, namespace_prefix, namespace_uri):
        self.namespace_prefix=namespace_prefix
        self.namespace_uri=namespace_uri
        self.namespace = Namespace(self.namespace_uri)
        self.graph = Graph()
        self.namespace_manager = self.graph.namespace_manager
        self.namespace_manager.bind(namespace_prefix, self.namespace)
        self.diseases = {}
        self.hasSymptom = URIRef(self.namespace_uri + "hasSymptom")

    def add_disease(self, disease):
        if disease in self.diseases:
            pass
        else:
            disease_URI = URIRef(self.namespace_uri + disease)
            self.diseases[disease] = disease_URI


    def add_symptom(self, disease, symptom):
        symptom_URI = URIRef(self.namespace_uri + symptom)
        if disease in self.diseases:
            disease_URI = self.diseases.get(disease)
        else:
            disease_URI = URIRef(self.namespace_uri + disease)
            self.diseases[disease] = disease_URI
        self.graph.add((disease_URI, self.hasSymptom, symptom_URI))

    def get_serialised_graph(self):
        return self.graph.serialize(format='pretty-xml')