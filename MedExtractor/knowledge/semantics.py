from knowledge.entity import Entity
from knowledge.relations import RelationType


class SemanticRelation:
    """
        A semantic relation between two entities connected by a value of RelationType.

        Additionally, a training sample can be saved that resulted in this semantic relation.
    """

    def __init__(self, entity_1: Entity, entity_2: Entity, relation_type: RelationType):
        self.entity_1 = entity_1
        self.entity_2 = entity_2
        self.relation_type = relation_type
        self.training_sample = None

