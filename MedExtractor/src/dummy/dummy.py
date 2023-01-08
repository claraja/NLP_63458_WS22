from src.interfaces.interfaces import PreprocessingInterface, KnowledgeExtractorInterface, RDFSerialiserInterface
from rdflib import Graph, Literal, Namespace
# rdflib knows about quite a few popular namespaces, like W3C ontologies, schema.org etc.
from rdflib.term import URIRef


class DummyPreprocessor(PreprocessingInterface):
    def get_preprocessed_text(self):
        with (open("resources/TextToAnalyzePreprocessed.txt")) as file:
            data = file.read()
        print ("preprocessing text.")
        return data

class DummyKnowledgeExtractor(KnowledgeExtractorInterface):
    def get_knowledge_base(self):
        print ("creating knowledge base")
        return "no idea how this is going to look"

class DummyRDFSerialiser(RDFSerialiserInterface):
    def serialise_knowledgebase(self):
        namespace_string = "http://fapranlp.de/"
        namespace = Namespace(namespace_string)
        # Create a Graph
        g = Graph()
        prefix = "fapra"
        namespace_manager = g.namespace_manager
        namespace_manager.bind(prefix, namespace)
        depression = URIRef(namespace_string +"depression")
        mentalDisorder = URIRef(namespace_string +"mentalDisorder")
        hasSymptom = URIRef(namespace_string +"hasSymptom")
        isA = URIRef(namespace_string +"isA")
        lom = Literal("lack of motivation")
        sadness = Literal("sadness")
        g.add((depression, isA, mentalDisorder))
        g.add((depression, hasSymptom, lom))
        g.add((depression, hasSymptom, sadness))
        return g.serialize(format='pretty-xml')
#%%
