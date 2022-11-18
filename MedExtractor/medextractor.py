from dummy.dummy import DummyPreprocessor, DummyKnowledgeExtractor, DummyRDFSerialiser
from rdf.RDFSerialiser import RDFSerialiser

with (open("resources/TextToAnalyze.txt")) as file:
    data = file.read()
preprocessor = DummyPreprocessor(data)
preprocessed_text = preprocessor.get_preprocessed_text()
# print(preprocessed_text)
knowledgeExtractor = DummyKnowledgeExtractor(preprocessed_text)
knowledgebase = knowledgeExtractor.get_knowledge_base()
# print(knowledgebase)
# rdfSerialiser = DummyRDFSerialiser(knowledgebase)
# print(rdfSerialiser.serialise_knowledgebase())
rdfSerialiser = RDFSerialiser(knowledgebase)
print("hi")
print(rdfSerialiser.serialise_knowledgebase())