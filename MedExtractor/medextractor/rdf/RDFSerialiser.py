from knowledge.entity import EntityType
from knowledge.relations import RelationType
from rdf.graphmanager import GraphManager


class RDFSerialiser():

    def __init__(self, knowledgebase, namespace, namespace_prefix):
        """Initialises the RDFSerialiser with a knowledgebase and the 
        namespace and namespace-prefix for thr RDF-output-generation.

        Parameters
        ----------
        knowledgebase : KnowledgeBase
        namespace : string
            namespace prefix for creating the RDF-output
        namespace_prefix : string
            namespace URI for creating the RDF-output

        Returns
        -------
        None
        """
        self._knowledgebase = knowledgebase
        self._namespace = namespace
        self._namespace_prefix = namespace_prefix
        self._serialisation_format = 'pretty-xml'
        self._graphmanager = GraphManager(self._namespace_prefix, self._namespace)

    def serialise_knowledgebase(self, output_path):
        """Serialises knowledge base into an RDF file.

        Parameters
        ----------
        output_path: string
            path to which the xml-document resulting from the rdflib-Graph will be saved

        Returns
        -------
        None
        """
        self.knowledgebase_to_graph()
        self._graphmanager.get_serialized_graph(
            output_path, self._serialisation_format)

    def knowledgebase_to_graph(self):
        """Transfers the content of the knowledgebase into an rdflib-graph.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for semantic_relation in self._knowledgebase.semantic_relations:
            entity_1_name = semantic_relation.entity_1.entity_name.replace(
                ' ', '_')
            entity_1_type = semantic_relation.entity_1.entity_type
            entity_2_name = semantic_relation.entity_2.entity_name.replace(
                ' ', '_')
            entity_2_type = semantic_relation.entity_2.entity_type
            relation_type = semantic_relation.relation_type

            if entity_1_type == EntityType.DISEASE:
                if entity_2_type == EntityType.SYMPTOM and relation_type == RelationType.HAS_SYMPTOM:
                    self._graphmanager.add_symptom(
                        entity_1_name, entity_2_name)
            elif entity_1_type == EntityType.SYMPTOM:
                if entity_2_type == EntityType.DISEASE and relation_type == RelationType.IS_SYMPTOM_OF:
                    self._graphmanager.add_symptom(
                        entity_2_name, entity_1_name)


# %%
