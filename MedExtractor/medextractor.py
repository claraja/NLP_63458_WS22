from src.rdf.RDFSerialiser import RDFSerialiser
from src.config_manager import ConfigManager
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

# Load configuration file
config = ConfigManager()

# Create main class for processing and extracting knowledge
knowledgeExtractor = KnowledgeExtractor(config)

# Process texts about mental diseases
knowledgeExtractor.process_texts()

# Optional step: save knowledge base
knowledgeExtractor.saveKB()

# Optional step: save data for future use with entity linker
knowledgeExtractor.export_for_entity_linker(config.entity_linker_export_filename)

# Create RDF serialisation class
rdfSerialiser = RDFSerialiser(knowledgeExtractor.get_knowledge_base(), 'http://fapranlp.de/', 'nlp')

# Serialise knowledge base into RDF file
rdfSerialiser.serialise_knowledgebase(config.relations_filename)