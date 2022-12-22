from dummy.dummy import DummyPreprocessor, DummyKnowledgeExtractor, DummyRDFSerialiser
from rdf.RDFSerialiser import RDFSerialiser
from preprocessor.preprocessor import RuleBasedPreprocessor
from knowledge_extractor.knowledge_extractor import KnowledgeExtractor
import spacy

#with (open("resources/TextToAnalyze.txt")) as file:
#     data = file.read()

text_to_analyze = "resources/TextToAnalyze.txt"
#text_to_analyze = "resources/Bulimia.txt"
#preprocessor = DummyPreprocessor(data)
preprocessor = RuleBasedPreprocessor(text_to_analyze)
preprocessed_text = preprocessor.get_preprocessed_text()
#print(preprocessed_text)
nlp = spacy.load('en_core_web_sm')
knowledgeExtractor = KnowledgeExtractor('test.kb',nlp)
rdfSerialiser = RDFSerialiser('http://fapranlp.de/', 'nlp')
graph = rdfSerialiser.create_graph()
for sent in nlp(preprocessed_text).sents:
    print(sent.text)
    knowledgeExtractor(sent.text)
    
knowledgebase = knowledgeExtractor.get_knowledge_base()
print(f"knowledgebase: {knowledgebase._semantic_relations[0].entity_1.entity_type}")
graph = rdfSerialiser.knowledgebase_to_graph(knowledgebase, graph)

rdfSerialiser.serialize_graph(graph, 'test.xml')

print("hi")
#print(rdfSerialiser.serialise_knowledgebase())