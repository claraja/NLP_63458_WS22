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
print(preprocessed_text)
nlp = spacy.load('en_core_web_sm')
knowledgeExtractor = KnowledgeExtractor('MedExtractor\\test.kb',nlp)

span = nlp("the blues")[0:2]
span.label_ = "DISEASE"

context = set()
context.add(span)
knowledgeExtractor.set_context(context)

for sent in nlp(preprocessed_text).sents:
    knowledgeExtractor(sent.text)

knowledgebase = knowledgeExtractor.get_knowledge_base()

for semantic_relation in knowledgebase._semantic_relations:
    print(semantic_relation.__str__())

# print(knowledgebase)
# rdfSerialiser = DummyRDFSerialiser(knowledgebase)
# print(rdfSerialiser.serialise_knowledgebase())
rdfSerialiser = RDFSerialiser(knowledgebase, 'http://fapranlp.de/', 'nlp')
graph = rdfSerialiser.create_graph()
graph = rdfSerialiser.knowledgebase_to_graph(knowledgebase, graph)
#rdfSerialiser.set_serialisation_format('...')
rdfSerialiser.serialize_graph(graph, 'test.xml')

print("hi")
#print(rdfSerialiser.serialise_knowledgebase())