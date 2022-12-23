from rdf.RDFSerialiser import RDFSerialiser
from preprocessor.preprocessor import RuleBasedPreprocessor
from knowledge_extractor.knowledge_extractor import KnowledgeExtractor
import spacy

text_to_analyze = "resources/TextToAnalyze.txt"
preprocessor = RuleBasedPreprocessor(text_to_analyze)
preprocessed_text = preprocessor.get_preprocessed_text()

nlp = spacy.load('en_core_web_sm')

knowledgeExtractor = KnowledgeExtractor('MedExtractor\\test.kb',nlp)

span = nlp("the blues")[0:2]
span.label_ = "DISEASE"

context = set()
context.add(span)
knowledgeExtractor.set_context(context)

rdfSerialiser = RDFSerialiser('/', 'nlp_fapra')
graph = rdfSerialiser.create_graph()

for sent in nlp(preprocessed_text).sents:
    knowledgeExtractor(sent.text)

knowledgeExtractor.saveKB()
knowledgebase = knowledgeExtractor.get_knowledge_base()

for semantic_relation in knowledgebase._semantic_relations:
    print(semantic_relation.__str__())

# print(knowledgebase)
# rdfSerialiser = DummyRDFSerialiser(knowledgebase)
# print(rdfSerialiser.serialise_knowledgebase())

rdfSerialiser = RDFSerialiser(knowledgebase, 'http://fapranlp.de/', 'nlp')
graph = rdfSerialiser.create_graph()
graph = rdfSerialiser.knowledgebase_to_graph(knowledgebase, graph)

rdfSerialiser.serialize_graph(
    graph=graph, 
    output_path='extracted_relations.xml', 
    serialization_format='pretty-xml' # default='pretty-xml'; möglich auch 'xml' und weitere, siehe: https://rdflib.readthedocs.io/en/stable/plugin_serializers.html
    )
