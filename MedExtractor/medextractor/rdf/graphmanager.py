from rdflib import Graph, Namespace
from rdflib.term import URIRef


class GraphManager:
    def __init__(self, namespace_prefix, namespace_uri):
        """When initializing the GraphManager an rdflib-graph is generated and 
        other instances used to develop and later serialise the graph are initialised.

        Parameters
        ----------
        namespace_prefix : string
            namespace prefix for creating the RDF-output
        namespace_uri : string
            namespace URI for creating the RDF-output

        Returns
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

        Parameters
        ----------
        disease : string
        symptom : string

        Returns
        -------
        None
        """
        symptom_URI = URIRef(self.namespace_uri + f"symptom:{symptom}")
        if f"disease:{disease}" in self.diseases:
            disease_URI = self.diseases.get(f"disease:{disease}")
        else:
            disease_URI = URIRef(self.namespace_uri + disease)
            self.diseases[disease] = disease_URI
        self.graph.add((disease_URI, self.hasSymptom, symptom_URI))

    def get_serialized_graph(self, output_path, serialization_format='pretty-xml'):
        return self.graph.serialize(format=serialization_format, destination=output_path)
