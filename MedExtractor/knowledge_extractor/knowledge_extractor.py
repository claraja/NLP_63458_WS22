import os
import pickle
import time

import _pickle as cPickle
from pathlib import Path

import spacy

from interfaces.interfaces import KnowledgeExtractorInterface
from knowledge.base import KnowledgeBase
from knowledge.entity import Entity
from knowledge.entity import EntityType
from knowledge.relations import RelationType
from knowledge.semantics import SemanticRelation
import spacy_transformers
from negspacy.negation import Negex

class KnowledgeExtractor(KnowledgeExtractorInterface):
    def __init__(self,*args):
        super().__init__(*args)
        time_tmp = time.time()
        p = os.path.join('knowledge_extractor', 'config.cfg')
        with open(p, 'rb') as f:
            config = pickle.load(f)
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        self._nlp = lang_cls.from_config(config)
        print(f'time load config: {time.time() - time_tmp}s')
        time_tmp = time.time()
        p = os.path.join('knowledge_extractor', 'pipeline.bin')
        with open(p, 'rb') as f:
            bytes_data = f.read()
        self._nlp.from_bytes(bytes_data)
        print(f'time load pipeline: {time.time() - time_tmp}s')
        self._doc = self._nlp("")
        self._kb = KnowledgeBase()
        self._context = []

        if (self._kb_filename != "") and os.path.exists(self._kb_filename):
            self._kb.load(self._kb_filename)


    def __call__(self,text):

        self._doc = self._nlp(text)

        for sent in self._doc.sents:
            entities = set()

            for ent in sent.ents:
                entities.add(ent)
            entities = list(entities)
            entities += self._context

            for ent1 in entities:
                for ent2 in entities:
                    res = self._is_related(ent1, ent2, sent)
                    if res != RelationType.NO_RELATION:
                        if (ent1.label_ == "DISEASE"):
                            entity1 = Entity(ent1.text,EntityType.DISEASE)
                        elif (ent1.label_ == "SYMPTOM"):
                            if ent1._.negex == False:
                                entity1 = Entity(ent1.text,EntityType.SYMPTOM)
                            else:
                                entity1 = Entity('no ' + ent1.text,EntityType.SYMPTOM)

                        else:
                            entity1 = Entity(ent1.text,EntityType.UNDEFINED)

                        if (ent2.label_ == "DISEASE"):
                            entity2 = Entity(ent2.text,EntityType.DISEASE)
                        elif (ent2.label_ == "SYMPTOM"):
                            if ent2._.negex == False:
                                entity2 = Entity(ent2.text,EntityType.SYMPTOM)
                            else:
                                entity2 = Entity('no ' + ent2.text,EntityType.SYMPTOM)
                        else:
                            entity2 = Entity(ent2.text,EntityType.UNDEFINED)

                        relation = SemanticRelation(entity1,entity2,res)
                        if not self._kb.has_relation(relation):
                            self._kb.add_relation(relation)

    def set_context(self, context):
        self._context = context
        return

    def get_knowledge_base(self):
        return self._kb
    
    def _is_related(self,entity1,entity2,sent):

        relation = RelationType.NO_RELATION

        if entity1.label_ == "DISEASE" and entity2.label_ == "SYMPTOM":
            relation = RelationType.HAS_SYMPTOM
        
        if entity1.label_ == "SYMPTOM" and entity2.label_ == "DISEASE":
            relation = RelationType.IS_SYMPTOM_OF

        return relation
    
    def saveKB(self,*args):
        error = True
        if len(args) == 0:
            self._kb.save(self._kb_filename)    
            error = False 
        elif len(args) == 1:
            if isinstance(args[0],str):
                self._kb_filename = args[0]
                self._kb.save(self._kb_filename)    
                error = False
        if error == True:
            print("Fehlerhafte Argumente beim Speichern der Wissensbasis")  # Fehlerhandling muss noch implementiert werden
        return

    def call2(self,text):

        self._doc = self._nlp(text)

        for sent in self._doc.sents:
            entities = set()

            for ent in sent.ents:
                entities.add(ent)
            entities = list(entities)
            entities += self._context

            # for ent1 in entities:
                # dependency parser
                # get subject
                # get object
                # get predicate


                # relation = SemanticRelation(entity1,entity2,res)
                # if not self._kb.has_relation(relation):
                #     self._kb.add_relation(relation)
