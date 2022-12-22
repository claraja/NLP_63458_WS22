from interfaces.interfaces import RDFSerialiserInterface
from rdflib import Graph, Literal, Namespace
from rdflib.term import URIRef
from graphmanager import GraphManager
from knowledge.entity import EntityType
from knowledge.relations import RelationType

class RDFSerialiser(RDFSerialiserInterface):
    #def serialise_knowledgebase(self):
    #    graph = GraphManager("fapra", "http://fapranlp.de/")
    #    graph.add_disease("depression")
    #    graph.add_symptom("depression", "lack_of_motivation")
    #    graph.add_symptom("depression", "sadness")
    #    return graph.get_serialised_graph()

    def knowledgebase_to_graph(self, knowledgebase, graph):
        for semantic_relation in knowledgebase._semantic_relations:
            entity_1_name = semantic_relation.entity_1.entity_name.replace(' ', '_')
            entity_1_type = semantic_relation.entity_1.entity_type
            entity_2_name = semantic_relation.entity_2.entity_name.replace(' ', '_')
            entity_2_type = semantic_relation.entity_2.entity_type
            relation_type = semantic_relation.relation_type

            if entity_1_type==EntityType.DISEASE:
                graph.add_disease(entity_1_name)
                if entity_2_type==EntityType.SYMPTOM and relation_type==RelationType.HAS_SYMPTOM:
                    graph.add_symptom(entity_1_name, entity_2_name)
            elif entity_1_type==EntityType.SYMPTOM:
                if entity_2_type==EntityType.DISEASE and relation_type==RelationType.IS_SYMPTOM_OF:
                    graph.add_symptom(entity_2_name, entity_1_name)
        
        """
        graph.add_disease("depression")
        graph.add_symptom("depression", "lack_of_motivation")
        graph.add_symptom("depression", "sadness")
        """
        return  graph

    def create_graph(self):
        return GraphManager(self.namespace_prefix, self.namespace)
#%%
