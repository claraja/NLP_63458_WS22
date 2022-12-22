from abc import ABC, abstractmethod
from spacy import Language

class PreprocessingInterface(ABC):

    def __init__(self, doc_name):
        self.doc_name = doc_name
        super().__init__()

    @abstractmethod
    def get_preprocessed_text(self) -> str:
        raise NotImplementedError

class KnowledgeExtractorInterface(ABC):

    def __init__(self, *args):
        error = True
        if len(args) == 1:
            if isinstance(args[0],Language):
                self._kb_filename = ""
                self._nlp = args[0]
                error = False
        elif len(args) == 2:
            if isinstance(args[0],str) and isinstance(args[1],Language):
                self._kb_filename = args[0]
                self._nlp = args[1]
                error = False
        if error == True:
            print("Fehlerhafte Argumente bei Erzeugung des KnowledgeExtractors")  # Fehlerhandling muss noch implementiert werden

    @abstractmethod
    def get_knowledge_base(self) -> str:
        raise NotImplementedError

class RDFSerialiserInterface(ABC):

    def __init__(self, knowledgebase, namespace, namespace_prefix):
        self.knowledgebase = knowledgebase
        self.namespace = namespace
        self.namespace_prefix = namespace_prefix
        #self.serialisation_format = 'pretty-xml'
        super().__init__()

    #@abstractmethod
    #def serialise_knowledgebase(self) -> str:
    #    raise NotImplementedError

    #@abstractmethod
    def serialize_graph(self, graph, output_path):
        #graph.serialize(format='pretty-xml', destination=output_path)
        #output = graph.get_serialised_graph()
        #raise NotImplementedError
        graph.get_serialized_graph(output_path)

    #@abstractmethod
    def set_serialisation_format(self, serialisation_format):
        self.serialisation_format = serialisation_format
