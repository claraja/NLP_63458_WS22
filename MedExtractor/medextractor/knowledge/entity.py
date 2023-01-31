from enum import Enum


class EntityType(Enum):
    """Types of entities that can be stored in the KnowledgeBase."""


    DISEASE = 1
    SYMPTOM = 2
    UNDEFINED = 3


class Entity:
    """An entity consisting of its name string and its EntityType"""
    def __init__(self, entity_name: str, entity_type: EntityType):
        """Upon initialization of the Entity the entity_name and its type are set.

        Parameters
        ----------
        entity_name: string
            The name of the entity
        entity_type: EntityType
            The type of the entity

        Returns
        -------
        None
        """
        self.entity_name = entity_name
        self.entity_type = entity_type

    def __str__(self) -> str:
        s = str(self.entity_name) + " (" + str(self.entity_type) + ")"
        return s

    def __eq__(self, other):
        return (self.entity_name, self.entity_type) == (other.entity_name, other.entity_type)