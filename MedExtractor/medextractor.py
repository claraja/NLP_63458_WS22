from src.config_manager import ConfigManager
from src.knowledge_extractor.knowledge_extractor import KnowledgeExtractor
from src.rdf.RDFSerialiser import RDFSerialiser

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
