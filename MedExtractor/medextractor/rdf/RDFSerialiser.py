from interfaces.interfaces import RDFSerialiserInterface
from knowledge.entity import EntityType
from knowledge.relations import RelationType


class RDFSerialiser(RDFSerialiserInterface):

    def serialise_knowledgebase(self, output_path):
        self.knowledgebase_to_graph()
        self._graphmanager.get_serialized_graph(
            output_path, self._serialisation_format)

    def set_serialisation_format(self, serialisation_format):
        self._serialisation_format = serialisation_format

    def knowledgebase_to_graph(self):
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
