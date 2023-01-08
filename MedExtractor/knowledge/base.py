from knowledge.semantics import SemanticRelation
from knowledge.entity import Entity
from knowledge.entity import EntityType
import string
import pickle
import os


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
        self._entities = []
        self._aliases = []
        self._training_samples = []
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

    def give_relation(self, relation: SemanticRelation) -> SemanticRelation:
        for other in self.semantic_relations:
            if other == relation:
                return other
        return None

    def give_entities(self,alias):
        alias_entity = Entity(alias,EntityType.SYMPTOM)
        result = []
        for relation in self.semantic_relations:
            if relation.entity_2 == alias_entity:
                result.append(relation.entity_1)
        return result


    def export_for_entity_linker(self, file_name: str):
        
        if (file_name != ""):
            fobj = open(file_name,'w', encoding="utf-8")
            fobj.write("### TRAINING DATA ###" + "\n")
            fobj.close
            fobj = open(file_name,'a', encoding="utf-8")

        for relation in self.semantic_relations:
            for sample in relation.training_samples:
                output = "('" + sample + "'"
                output_aux = ",{"
                first1 = True
                for alias in self._aliases:
                    if alias in sample:
                        if first1 != True:
                            output_aux += ","
                        output += ",[(" + str(sample.find(alias)) + "," + str(sample.find(alias) + len(alias)) + ",'SYMPTOM')]"
                        output_aux += "(" + str(sample.find(alias)) + "," + str(sample.find(alias) + len(alias)) + "):"
                        output_aux += "{"
                        first2 = True
                        for ent in self.give_entities(alias):
                            if first2 != True:
                                output_aux += ","
                            if ent.entity_name in sample:
                                output_aux += "'" + ent.entity_name + "': 1.0"
                            else:
                                output_aux += "'" + ent.entity_name + "': 0.0"
                            first2 = False
                        first1 = False
                        output_aux += "}"
                output += output_aux + "}"
                output += ",[1"
                
                for word in sample.strip(string.punctuation).split():
                    if word.isalpha():
                        output += ",-1"

                output += "])"
                if fobj != None:
                    fobj.write(output + "\n")
        fobj.close()

    def save(self, file_name: str) -> None:
        with open(file_name, 'wb') as file:
            pickle.dump(self.semantic_relations, file)
            pickle.dump(self._entities, file)
            pickle.dump(self._aliases, file)

    def load(self, file_name: str):
        with open(file_name, 'rb') as file:
            self.semantic_relations = pickle.load(file)
            self._entities = pickle.load(file)
            self._aliases = pickle.load(file)
            return self
