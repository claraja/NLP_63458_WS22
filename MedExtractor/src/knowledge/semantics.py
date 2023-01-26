from src.knowledge.entity import Entity
from src.knowledge.relations import RelationType


class SemanticRelation:
    """A semantic relation between two entities connected by a value of RelationType.

    Additionally, training samples can be saved that resulted in this semantic relation.
    """

    def __init__(self, entity_1: Entity, entity_2: Entity, relation_type: RelationType, training_sample: str = None):
        """Upon initialization of the SemanticRelation the two entities and the RelationType are set.
        The list of training samples is initialised and optionally appended with the first training sample.

        Parameters:
        ----------
        text: string
            The text string to be analyzed by the KnowledgeExtractor
        entity_1: Entity
            The first Entity
        entity_2: Entity
            The second entity
        relation_type: RelationType
            The RelationType that connects both entities
        training_sample: str = None
            An optional first training sample

        Returns:
        -------
        None
        """
        self.entity_1 = entity_1
        self.entity_2 = entity_2
        self.relation_type = relation_type
        self.training_samples = []
        if relation_type == None:
            self.training_samples.append(training_sample)


    def __str__(self) -> str:
        s = str(self.entity_1) + " - " + str(self.relation_type) + " - " + str(self.entity_2)
        return s

    def __eq__(self, other):
        return (self.entity_1, self.entity_2, self.relation_type) == (other.entity_1, other.entity_2, other.relation_type)

    def contains_training_sample(self, training_sample: str) -> bool:
        """Checks whether the training_sample given is already included in the list of training samples.

        Parameters:
        ----------
        training_sample: string
            A text sample/sentence

        Returns:
        -------
            true, if training_sample is contained in the list, false otherwise
        """
        return training_sample in self.training_samples

    def add_training_sample(self, training_sample: str):
        """Adds the training_sample into the list of training_samples.

        Parameters:
        ----------
        training_sample: string
            The text sample/sentence to be added

        Returns:
        -------
        None
        """
        if not self.contains_training_sample(training_sample):
            self.training_samples.append(training_sample)
