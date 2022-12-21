from enum import Enum


class EntityType(Enum):
    """
        Types of entities that can be stored in the KnowledgeBase.
    """

    DISEASE = 1
    SYMPTOM = 2
    UNDEFINED = 3


class Entity:

    def __init__(self, entity_name: str, entity_type: EntityType):
        self.entity_name = entity_name
        self.entity_type = entity_type

    def __str__(self) -> str:
        s = str(self.entity_name) + " (" + str(self.entity_type) + ")"
        return s

