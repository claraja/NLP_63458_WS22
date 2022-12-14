import os
import string

from src.knowledge.semantics import SemanticRelation
from src.knowledge.entity import Entity
from src.knowledge.entity import EntityType
import string
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
            fobj.write("### ENTITIES ###" + "\n")
            fobj.close
            fobj = open(file_name,'a', encoding="utf-8")

        for entity in sorted(self._entities):
            fobj.write(entity + "\n")

        fobj.write("### ALIASES ###" + "\n")
        for alias in sorted(self._aliases):
            #fobj.write("alias = '" + alias + "', entities = [")
            fobj.write(alias + '\n')
            first = True;
            fobj.write("Entities:")
            for relation in self.semantic_relations:
                if relation.entity_2.entity_name == alias:
                    if first == False:
                        fobj.write("<sep>")
                    #fobj.write("'" + relation.entity_1.entity_name + "'")
                    fobj.write(relation.entity_1.entity_name)
                    first = False
            #fobj.write("]\n")
            fobj.write("\n")

        fobj.write("### TRAINING DATA ###" + "\n")
        for relation in self.semantic_relations:
            for sample in relation.training_samples:
                sample = sample.replace("\"","")
                sample = sample.replace("\n"," ")
                output = "(\"" + sample + "\", ["
                output_aux = ",{"
                first1 = True
                indexes = []
                for alias in self._aliases:
                    if alias in sample:
                        start = sample.find(alias)
                        end = sample.find(alias) + len(alias)
                        should_add = True
                        for i in indexes:
                            if not ((end < i[0]) or (start > i[1])):
                                should_add = False
                                break
                        if should_add == True:
                            indexes.append((start,end))
                            if first1 != True:
                                output += ","
                                output_aux += ","
                            output += "(" + str(start) + "," + str(end) + ",'SYMPTOM')"
                            output_aux += "(" + str(start) + "," + str(end) + "):"
                            output_aux += "{"
                            first2 = True
                            entity_list = self.give_entities(alias)
                            entity_count = 0
    
                            for ent in entity_list:
                                if ent.entity_name in sample:
                                    entity_count += 1

                            for ent in entity_list:
                                if first2 != True:
                                    output_aux += ","
                                if ent.entity_name in sample:
                                    output_aux += "'" + ent.entity_name + "': {:.1f}".format(1.0/entity_count)
                                else:
                                    output_aux += "'" + ent.entity_name + "': 0.0"
                                first2 = False
                            first1 = False
                            output_aux += "}"
                output += ']' + output_aux + "}"
                output += ",[1"
                
                for word in sample.translate(str.maketrans('', '', string.punctuation)).split():
                    if word.isalpha():
                        output += ",-1"

                output += "])"
                if fobj != None:
                    fobj.write(output + "\n")
        if fobj != None:
            fobj.write("### END ###\n")
            fobj.close()

    def save(self, file_name: str) -> None:
        # TODO: improve filehandling if knowledge base doesn't exist, yet
        if file_name == '':
            file_name = os.path.join('resources', 'test.kb')
        with open(file_name, 'wb') as file:
            pickle.dump([self.semantic_relations, self._entities, self._aliases], file)

    def load(self, file_name: str):
        if file_name == '':
            return KnowledgeBase()
        with open(file_name, 'rb') as file:
            self.semantic_relations, self._entities, self._aliases = pickle.load(file)
            return self
