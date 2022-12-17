import sys
sys.path.append("D:\Git_Fachpraktikum")
sys.path.append("D:\Git_Fachpraktikum\MedExtractor")
sys.path.append("D:\Git_Fachpraktikum\MedExtractor\knowledge_extractor")

import spacy
from spacy.pipeline import EntityRecognizer
from spacy.training import Example
from knowledge_extractor import KnowledgeExtractor

nlp = spacy.load('en_core_web_sm')
ke = KnowledgeExtractor("test_kb", nlp)