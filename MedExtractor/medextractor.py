from dummy.dummy import DummyPreprocessor, DummyKnowledgeExtractor, DummyRDFSerialiser
from rdf.RDFSerialiser import RDFSerialiser
from preprocessor.preprocessor import RuleBasedPreprocessor

#with (open("resources/TextToAnalyze.txt")) as file:
#     data = file.read()

text_to_analyze = "resources/TextToAnalyze.txt"
#text_to_analyze = "resources/Bulimia.txt"
#preprocessor = DummyPreprocessor(data)
preprocessor = RuleBasedPreprocessor(text_to_analyze)
preprocessed_text = preprocessor.get_preprocessed_text()
print(preprocessed_text)
knowledgeExtractor = DummyKnowledgeExtractor(preprocessed_text)
knowledgebase = knowledgeExtractor.get_knowledge_base()
# print(knowledgebase)
# rdfSerialiser = DummyRDFSerialiser(knowledgebase)
# print(rdfSerialiser.serialise_knowledgebase())
rdfSerialiser = RDFSerialiser(knowledgebase)
print("hi")
print(rdfSerialiser.serialise_knowledgebase())