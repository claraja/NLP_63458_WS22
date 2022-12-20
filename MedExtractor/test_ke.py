import sys
import spacy

sys.path.append('MedExtractor')
sys.path.append('MedExtractor\\knowledge_extractor')

from knowledge_extractor.knowledge_extractor import KnowledgeExtractor

nlp = spacy.load('en_core_web_sm')
ke = KnowledgeExtractor(nlp)

text_file = open('resources\\TextToAnalyzePreprocessed.txt','r')
text = text_file.read()
ke(text)