from knowledge.semantics import SemanticRelation
import pickle


class KnowledgeBase(object):
    '''
        The KnowledgeBase Singleton manages entities and relations.

        Functions:
        add_relation(SemanticRelation)
        has_relation(SemanticRelation) -> bool
        export_for_entity_linker(str)
        safe(str) -> None
        load(str) -> KnowledgeBase
    '''
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KnowledgeBase, cls).__new__(cls)
            # Put any initialization here.
            cls._semantic_relations = []
            cls._entities: []
        return cls._instance

    def add_relation(self, relation: SemanticRelation):
        self._semantic_relations.append(relation)

    def has_relation(self, relation: SemanticRelation) -> bool:
        return relation in self._semantic_relations

    def export_for_entity_linker(self, file_name: str):
        pass

    def safe(self, file_name: str) -> None:
        with open(file_name, 'wb') as file:
            pickle.dump(self._instance, file)

    def load(self, file_name: str):
        with open(file_name, 'rb') as file:
            self._instance = pickle.load(file)
            return self._instance
