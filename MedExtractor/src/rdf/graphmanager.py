from rdflib import Graph, Namespace
from rdflib.term import URIRef


class GraphManager:
    def __init__(self, namespace_prefix, namespace_uri):
        """Bei Initialisierung des GraphManagers wird ein rdflib-Graph erstellt ...TODO

        Parameters:
        ----------
        namespace_prefix: string
            TODO:Beschreibung
        namespace_uri: string
            TODO:Beschreibung

        Returns:
        -------
        None
        """
        self.namespace_prefix = namespace_prefix
        self.namespace_uri = namespace_uri
        self.namespace = Namespace(self.namespace_uri)
        self.graph = Graph()
        self.namespace_manager = self.graph.namespace_manager
        self.namespace_manager.bind(namespace_prefix, self.namespace)
        self.diseases = {}
        self.hasSymptom = URIRef(self.namespace_uri + "hasSymptom")

    def add_symptom(self, disease, symptom):
        """Adds the found symptom together with the corresponding disease the the rdflib-graph.

        Parameters:
        ----------
        diesease: string
        symptom: string

        Returns:
        -------
        None
        """
        symptom_URI = URIRef(self.namespace_uri + f"symptom:{symptom}")
        if f"disease:{disease}" in self.diseases:
            disease_URI = self.diseases.get(f"disease:{disease}")
        else:
            disease_URI = URIRef(self.namespace_uri + f"disease:{disease}")
            self.diseases[f"disease:{disease}"] = disease_URI
        self.graph.add((disease_URI, self.hasSymptom, symptom_URI))

    def get_serialized_graph(self, output_path, serialization_format='pretty-xml'):
        return self.graph.serialize(format=serialization_format, destination=output_path)
