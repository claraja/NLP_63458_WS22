from src.rdf.RDFSerialiser import RDFSerialiser
from src.preprocessor.preprocessor import RuleBasedPreprocessor
from src.knowledge_extractor.knowledge_extractor import KnowledgeExtractor
import os, glob
import spacy
import time

print("cwd: " + os.getcwd())
nlp = spacy.load('en_core_web_sm')
time_tmp = time.time()
knowledgebase_path = os.path.join('resources', 'test.kb')
knowledgeExtractor = KnowledgeExtractor(knowledgebase_path, nlp)
print(f'time create knowledgeExtractor: {time.time()-time_tmp}s')
time_tmp = time.time()
knowledgebase = knowledgeExtractor.get_knowledge_base()
print(f'time get knowledgebase: {time.time()-time_tmp}s')
print(f"size of knowledgebase:  {len(knowledgebase)}")

time_tmp = time.time()
for filename in glob.glob('resources/to_analyze_small/*.txt'):
    preprocessor = RuleBasedPreprocessor(filename)
    preprocessed_text = preprocessor.get_preprocessed_text()

    #print('\nBereits in der Wissensbasis (' + str(len(knowledgebase.semantic_relations)) + '):')
    #for semantic_relation in knowledgeExtractor.get_knowledge_base().semantic_relations:
    #    print(semantic_relation.__str__())

    #span = nlp("the blues")[0:2]
    #span.label_ = "DISEASE"
    #context = set()
    #context.add(span)
    #knowledgeExtractor.set_context(context)

    #rdfSerialiser = RDFSerialiser('/', 'nlp_fapra')
    #graph = rdfSerialiser.create_graph()
    
    for sent in nlp(preprocessed_text).sents:
        knowledgeExtractor(sent.text)

knowledgeExtractor.saveKB()

#print('\nNach neuer Analyse in der Wissensbasis (' + str(len(knowledgebase.semantic_relations)) + '):')
#for semantic_relation in knowledgebase.semantic_relations:
#    print(semantic_relation.__str__())

knowledgebase.export_for_entity_linker("resources/entity_linker_export.txt")
print(f"size of knowledgebase:  {len(knowledgebase)}")

print(f'time complete loop over files: {time.time()-time_tmp}s')
# print(knowledgebase)
# rdfSerialiser = DummyRDFSerialiser(knowledgebase)
# print(rdfSerialiser.serialise_knowledgebase())

time_tmp = time.time()
rdfSerialiser = RDFSerialiser('/', 'nlp')
graph = rdfSerialiser.create_graph()
graph = rdfSerialiser.knowledgebase_to_graph(knowledgebase, graph)
print(f'time convert kb to rdf-graph: {time.time()-time_tmp}s')

time_tmp = time.time()
output_path = os.path.join('resources', 'extracted_relations.xml')
rdfSerialiser.serialize_graph(
    graph=graph,
    output_path=output_path,
    serialization_format='pretty-xml' # default='pretty-xml'; möglich auch 'xml' und weitere, siehe: https://rdflib.readthedocs.io/en/stable/plugin_serializers.html
    )
print(f'time serialize graph and generate output-xml: {time.time()-time_tmp}s')
