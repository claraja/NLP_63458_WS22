from enum import Enum


class RelationType(Enum):
    """
        Types of relations to be used in the KnowledgeBase.
    """

    IS_SYMPTOM_OF = 1
    HAS_SYMPTOM = 2
    NO_RELATION = 3
