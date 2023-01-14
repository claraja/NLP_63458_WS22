import os
import string
import xml.etree.ElementTree as ElementTree
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
        
        entityLinker_xml = ElementTree.Element("entityLinkerExport")
        entity_node = ElementTree.SubElement(entityLinker_xml,"entities")
        
        for entity in sorted(self._entities):
            entity_xml = ElementTree.SubElement(entity_node, "entity", {"typ":"str"})
            entity_xml.text = entity
        
        alias_node = ElementTree.SubElement(entityLinker_xml,"aliases")
        for alias in sorted(self._aliases):
            
            alias_xml = ElementTree.SubElement(alias_node, "alias", {"typ":"str"})
            alias_xml.text = alias
            
            alias_entity_node = ElementTree.SubElement(alias_xml, "entities")
            for relation in self.semantic_relations:
                if relation.entity_2.entity_name == alias:
                    alias_entity_xml = ElementTree.SubElement(alias_entity_node, "entity", {"typ":"str"})
                    alias_entity_xml.text = relation.entity_1.entity_name

        training_node = ElementTree.SubElement(entityLinker_xml, "samples")    
        for relation in self.semantic_relations:
            for sample in relation.training_samples:

                sample_node = ElementTree.SubElement(training_node, "text")
                sample_node_xml = ElementTree.SubElement(sample_node, "text", {"typ":"str"})
                sample_node_xml.text = sample

                indices = []
                alias_training_node = ElementTree.SubElement(sample_node_xml, "aliases")
                linking_training_node = ElementTree.SubElement(sample_node_xml, "links")

                for alias in self._aliases:
                    if alias in sample:
                        start = sample.find(alias)
                        end = sample.find(alias) + len(alias)
                        should_add = True
                        for i in indices:
                            if not ((end < i[0]) or (start > i[1])):
                                should_add = False
                                break
                        if should_add == True:
                            indices.append((start,end))

                            alias_training_xml = ElementTree.SubElement(alias_training_node, "alias", {"typ":"tuple"})
                            alias_training_xml.text = "(" + str(start) + "," + str(end) + ",'SYMPTOM')"
                            
                            position_training_xml = ElementTree.SubElement(linking_training_node, "position", {"typ":"tuple"})
                            position_training_xml.text = "(" + str(start) + "," + str(end) + ")"

                            entity_list = self.give_entities(alias)
                            entity_count = 0
    
                            for ent in entity_list:
                                if ent.entity_name in sample:
                                    entity_count += 1
                            
                            entity_training_node = ElementTree.SubElement(position_training_xml, "entities")

                            for ent in entity_list:
                                
                                entity_training_xml = ElementTree.SubElement(entity_training_node, "entity", {"typ":"str"})
                                entity_training_xml.text = ent.entity_name

                                probability_training_node = ElementTree.SubElement(entity_training_xml, "prob")
                                probability_training_xml = ElementTree.SubElement(probability_training_node, "prob", {"typ":"float"})

                                if ent.entity_name in sample:
                                    probability_training_xml.text = str(round(1.0/entity_count,1))
                                else:
                                    probability_training_xml.text = "0.0"
                
                #for word in sample.translate(str.maketrans('', '', string.punctuation)).split():
                #    if word.isalpha():
                #        output += ",-1"

                #output += "])"
                #if fobj != None:
                #    fobj.write(output + "\n")
        if file_name != "":
            et = ElementTree.ElementTree(entityLinker_xml)
            et.write(file_name, encoding='UTF-8')

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
