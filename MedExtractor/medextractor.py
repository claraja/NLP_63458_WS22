from src.rdf.RDFSerialiser import RDFSerialiser
from src.preprocessor.preprocessor import RuleBasedPreprocessor
from src.knowledge_extractor.knowledge_extractor import KnowledgeExtractor
import os, glob
import spacy
import time
import json

print("cwd: " + os.getcwd())

try:
    with open("config.json", "r") as jsonfopen:
        json_read = json.load(jsonfopen)
except FileNotFoundError:
    jsoncontent = {
        "RDF_filename" : "path/name.xml",
        "EntityLinkerExport_filename" : "path/name.xml",
        "KnowledgeBase_filename" : "path/name.kb",
        "Sample_text_folder" : "path",
        "Overwrite existing knowledgebase file" : "False",
        "Diseases_filename" : "path/name.txt",
        "Symptoms_filename" : "path/name.txt",
    }
    with open("config.json", "w") as jsonfopen:
            json.dump(jsoncontent,jsonfopen, indent = 4)
    print("No file config.json in folder. New file was created as " + os.path.abspath(jsonfopen.name) + ". Please update this json-file before starting Medextractor again.")
    quit()

try:
    relations_filename = json_read["RDF_filename"]
except KeyError:
    print("No RDF file name in config.json.")
    quit()

try:
    entity_linker_export_filename = json_read["EntityLinkerExport_filename"]
except KeyError:
    print("No entity linker export file name in config.json.")
    quit()

try:
    knowledgebase_filename = json_read["KnowledgeBase_filename"]
except KeyError:
    print("No knowledgebase file name in config.json.")
    quit()

try:
    text_folder_name = json_read["Sample_text_folder"]
except KeyError:
    print("No text folder file name in config.json.")
    quit()

try:
    diseases_filename = json_read["Diseases_filename"]
except KeyError:
    print("No diseases file name in config.json.")
    quit()

try:
    symptoms_filename = json_read["Symptoms_filename"]
except KeyError:
    print("No symptoms file name in config.json.")
    quit()

try:
    overwrite = True if json_read["Overwrite existing knowledgebase file"] == "True" else False
except KeyError:
    print("No overwrite specification in config.json.")
    quit()

nlp = spacy.load('en_core_web_sm')
time_tmp = time.time()
#knowledgebase_path = os.path.join('resources', 'test.kb')
knowledgeExtractor = KnowledgeExtractor(knowledgebase_filename, nlp, diseases_filename, symptoms_filename, overwrite)
print(f'time create knowledgeExtractor: {time.time()-time_tmp}s')
knowledgebase = knowledgeExtractor.get_knowledge_base()
print(f"size of knowledgebase:  {len(knowledgebase)}")

time_tmp = time.time()
for filename in glob.glob(text_folder_name + "/*.txt"):
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
    
    for sent in nlp(preprocessed_text).sents:
        knowledgeExtractor(sent.text)

knowledgeExtractor.saveKB()

#print('\nNach neuer Analyse in der Wissensbasis (' + str(len(knowledgebase.semantic_relations)) + '):')
#for semantic_relation in knowledgebase.semantic_relations:
#    print(semantic_relation.__str__())

knowledgebase.export_for_entity_linker(entity_linker_export_filename)
print(f"size of knowledgebase:  {len(knowledgebase)}")

print(f'time complete loop over files: {time.time()-time_tmp}s')

rdfSerialiser = RDFSerialiser(knowledgebase, 'http://fapranlp.de/', 'nlp')

#output_path = os.path.join('resources', 'extracted_relations.xml')
#rdfSerialiser.serialise_knowledgebase( output_path=output_path) # default='pretty-xml'; möglich auch 'xml' und weitere, siehe: https://rdflib.readthedocs.io/en/stable/plugin_serializers.html
rdfSerialiser.serialise_knowledgebase(relations_filename) # default='pretty-xml'; möglich auch 'xml' und weitere, siehe: https://rdflib.readthedocs.io/en/stable/plugin_serializers.html