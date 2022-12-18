import sys
import csv
from spacy.pipeline import EntityRuler
from spacy.training import Example

sys.path.append('MedExtractor')
sys.path.append('MedExtractor\\knowledge')
sys.path.append('MedExtractor\\knowledge_extractor')

from interfaces.interfaces import KnowledgeExtractorInterface
from relations import RelationType

class KnowledgeExtractor(KnowledgeExtractorInterface):
    def __init__(self,kb_name,nlp):
        super().__init__(kb_name,nlp)
        self._nlp = nlp
        self._doc = nlp("")
        
        pipe_exceptions = ['tagger','parser']
        not_required_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        nlp.disable_pipes(*not_required_pipes)
        
        self._ruler = nlp.add_pipe("entity_ruler")
        
        input_data_file = open('MedExtractor\\knowledge_extractor\\training_diseases.txt','r',encoding="unicode_escape")
        reader = csv.reader(input_data_file, delimiter='\t')
        
        training_data = []
        
        for row in reader:
            to_train = {"label": "DISEASE", "pattern": row[1]}
            training_data.append(to_train)
        input_data_file.close()

        self._ruler.add_patterns(training_data)

        input_data_file = open('MedExtractor\\knowledge_extractor\\training_symptoms.txt','r',encoding="unicode_escape")
        reader = csv.reader(input_data_file, delimiter='\t')

        for row in reader:
            to_train = {"label": "SYMPTOM", "pattern": row[1]}
            training_data.append(to_train)
        input_data_file.close()

        self._ruler.add_patterns(training_data)


    def __call__(self,text):
        self._doc = self._nlp(text)
        
        entities = set()
        for ent in self._doc.ents:
            entities.add(ent)

        for ent1 in entities:
            for ent2 in entities:
                res = self._is_related(ent1, ent2)
                if res != RelationType.NO_RELATION:
                    print(ent1.text + " " + str(self._is_related(ent1, ent2)) + " " + ent2.text)

    def set_context(self):
        pass
    
    def get_knowledge_base(self):
        pass
    
    def _is_related(self,entity1,entity2):

        relation = RelationType.NO_RELATION
        
        if entity1.label_ == "DISEASE" and entity2.label_ == "SYMPTOM":
            relation = RelationType.HAS_SYMPTOM
        
        if entity1.label_ == "SYMPTOM" and entity2.label_ == "DISEASE":
            relation = RelationType.IS_SYMPTOM_OF

        if entity1 not in self._doc.ents or entity2 not in self._doc.ents:
            relation = RelationType.NO_RELATION
        
        return(relation)
        