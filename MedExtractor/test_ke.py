import sys
import spacy

sys.path.append('MedExtractor')
sys.path.append('MedExtractor\\knowledge_extractor')

from knowledge_extractor.knowledge_extractor import KnowledgeExtractor
from entity import Entity
from entity import EntityType

nlp = spacy.load('en_core_web_sm')
ke = KnowledgeExtractor(nlp)

text_file = open('resources\\TextToAnalyzePreprocessed.txt','r')

span = nlp("the blues")[0:2]
span.label_ = "DISEASE"

context = set()
context.add(span)
ke.set_context(context)

text = text_file.read()
ke(text)