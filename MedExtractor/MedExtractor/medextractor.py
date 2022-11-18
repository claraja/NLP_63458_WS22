from dummy.dummy import DummyPreprocessor, DummyKnowledgeExtractor, DummyRDFSerialiser
with (open("resources/TextToAnalyze.txt")) as file:
    data = file.read()
preprocessor = DummyPreprocessor(data)
preprocessed_text = preprocessor.get_preprocessed_text()
# print(preprocessed_text)
knowledgeExtractor = DummyKnowledgeExtractor(preprocessed_text)
knowledgebase = knowledgeExtractor.get_knowledge_base()
# print(knowledgebase)
rdfSerialiser = DummyRDFSerialiser(knowledgebase)
print(rdfSerialiser.serialise_knowledgebase())