import os
import spacy

#sys.path.append('MedExtractor')
#sys.path.append('MedExtractor\\knowledge_extractor')

from medextractor.knowledge_extractor.knowledge_extractor import KnowledgeExtractor

nlp = spacy.load('en_core_web_sm')
print("test knowledge extractor cwd: " + os.getcwd())
knowledge_base_path = os.path.join('../resources', 'test.kb')
ke = KnowledgeExtractor(knowledge_base_path,nlp)
# ke = KnowledgeExtractor("", nlp)
print('Anfang: ' + str(len(ke._kb.semantic_relations)))
text_path = os.path.join('../resources', 'to_analyze', 'TextToAnalyzePreprocessed.txt')
# text_file = open('resources\\TextToAnalyzePreprocessed.txt','r')
text_file = open(text_path,'r')

span = nlp("the blues")[0:2]
span.label_ = "DISEASE"

context = set()
context.add(span)
ke.set_context(context)

text = text_file.read()
ke(text)
ke.saveKB(knowledge_base_path)

print(os.getcwd())