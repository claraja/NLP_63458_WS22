import os
import spacy

from src.knowledge_extractor.knowledge_extractor import KnowledgeExtractor

nlp = spacy.load('en_core_web_sm')
print("test knowledge extractor cwd: " + os.getcwd())
knowledge_base_path = os.path.join( 'resources', 'testdependencykb.kb')
ke = KnowledgeExtractor(knowledge_base_path,nlp)
print('Anfang: ' + str(len(ke._kb.semantic_relations)))
text_path = os.path.join( 'resources', 'to_analyze', 'TextToAnalyzePreprocessed.txt')
with open(text_path,'r') as text_file:
    text = text_file.read()

ke.call2(text)
ke.saveKB(knowledge_base_path)

print(os.getcwd())