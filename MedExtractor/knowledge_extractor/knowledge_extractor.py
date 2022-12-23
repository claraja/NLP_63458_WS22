import sys
import csv
from spacy.pipeline import EntityRuler
from spacy.training import Example

from interfaces.interfaces import KnowledgeExtractorInterface
from knowledge.base import KnowledgeBase
from knowledge.entity import Entity
from knowledge.entity import EntityType
from knowledge.semantics import SemanticRelation
from knowledge.relations import RelationType

class KnowledgeExtractor(KnowledgeExtractorInterface):
    def __init__(self,*args):
        super().__init__(*args)
        self._doc = self._nlp("")
        self._kb = KnowledgeBase()
        self._context = []

        if (self._kb_filename != ""):
            self._kb.load(self._kb_filename)

        pipe_exceptions = ['tok2vec','tagger','parser']
        not_required_pipes = [pipe for pipe in self._nlp.pipe_names if pipe not in pipe_exceptions]
        self._nlp.disable_pipes(*not_required_pipes)
        
        self._ruler = self._nlp.add_pipe("entity_ruler")
        
        input_data_file = open('MedExtractor\\knowledge_extractor\\training_diseases_klein.txt','r',encoding="unicode_escape")
        reader = csv.reader(input_data_file, delimiter='\t')
        
        training_data = []
        
        for row in reader:
            to_train = {"label": "DISEASE", "pattern": row[1]}
            training_data.append(to_train)
        input_data_file.close()

        self._ruler.add_patterns(training_data)

        input_data_file = open('MedExtractor\\knowledge_extractor\\training_symptoms_klein.txt','r',encoding="unicode_escape")
        reader = csv.reader(input_data_file, delimiter='\t')

        for row in reader:
            to_train = {"label": "SYMPTOM", "pattern": row[1]}
            training_data.append(to_train)
        input_data_file.close()
        self._ruler.add_patterns(training_data)


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
                            entity1 = Entity(ent1.text,EntityType.SYMPTOM)
                        else:
                            entity1 = Entity(ent1.text,EntityType.UNDEFINED)

                        if (ent2.label_ == "DISEASE"):
                            entity2 = Entity(ent2.text,EntityType.DISEASE)
                        elif (ent2.label_ == "SYMPTOM"):
                            entity2 = Entity(ent2.text,EntityType.SYMPTOM)
                        else:
                            entity2 = Entity(ent2.text,EntityType.UNDEFINED)
                        
                        relation = SemanticRelation(entity1,entity2,res)
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