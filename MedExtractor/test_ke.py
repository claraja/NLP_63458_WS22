import sys
import spacy

sys.path.append('MedExtractor\\knowledge_extractor')

from knowledge_extractor import KnowledgeExtractor

nlp = spacy.load('en_core_web_sm')
ke = KnowledgeExtractor("test_kb", nlp)

text_file = open('resources\\TextToAnalyze.txt','r')
text = text_file.read()
ke(text.lower())