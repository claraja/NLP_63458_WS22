from knowledge.semantics import SemanticRelation
import pickle


class KnowledgeBase:
    '''
        The KnowledgeBase Singleton manages entities and relations.

        Functions:
        add_relation(SemanticRelation)
        has_relation(SemanticRelation) -> bool
        export_for_entity_linker(str)
        safe(str) -> None
        load(str) -> KnowledgeBase
    '''
    # _instance = None

    def __init__(self):
        # if cls._instance is None:
        # self._instance = super(KnowledgeBase, self).__new__(self)
        # Put any initialization here.
        self.semantic_relations = []
        self.allow_duplicates = False
        # self._entities = []
        # return cls._instance

    def __len__(self):
        return len(self.semantic_relations)

    def add_relation(self, relation: SemanticRelation):
        if self.allow_duplicates:
            self.semantic_relations.append(relation)
        else:
            if not self.has_relation(relation):
                self.semantic_relations.append(relation)


    def has_relation(self, relation: SemanticRelation) -> bool:
        for other in self.semantic_relations:
            if other == relation:
                return True
        return False

    def export_for_entity_linker(self, file_name: str):
        pass

    def save(self, file_name: str) -> None:
        with open(file_name, 'wb') as file:
            pickle.dump(self.semantic_relations, file)

    def load(self, file_name: str):
        with open(file_name, 'rb') as file:
            self.semantic_relations = pickle.load(file)
            return self
