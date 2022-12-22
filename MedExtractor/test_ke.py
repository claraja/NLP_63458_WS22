import sys
import spacy

#sys.path.append('MedExtractor')
#sys.path.append('MedExtractor\\knowledge_extractor')

from knowledge_extractor.knowledge_extractor import KnowledgeExtractor
from knowledge.entity import Entity
from knowledge.entity import EntityType

nlp = spacy.load('en_core_web_sm')
ke = KnowledgeExtractor('Medextractor\\test.kb',nlp)
print('Anfang: ' + str(len(ke._kb._semantic_relations)))
text_file = open('resources\\TextToAnalyzePreprocessed.txt','r')

span = nlp("the blues")[0:2]
span.label_ = "DISEASE"

context = set()
context.add(span)
ke.set_context(context)

text = text_file.read()
ke(text)
ke.saveKB('Medextractor\\test.kb')