from abc import ABC, abstractmethod
from spacy import Language

from rdf.graphmanager import GraphManager


class PreprocessingInterface(ABC):

    def __init__(self, doc_name):
        self.doc_name = doc_name
        super().__init__()

    @abstractmethod
    def get_preprocessed_text(self) -> str:
        raise NotImplementedError

class KnowledgeExtractorInterface(ABC):

    # def __init__(self, kb_filename, nlp):
    #     self._knowledgebase_filename = kb_filename
    #     self._nlp = nlp

    @abstractmethod
    def get_knowledge_base(self) -> str:
        raise NotImplementedError

class RDFSerialiserInterface(ABC):

    def __init__(self, knowledgebase, namespace, namespace_prefix):
        """Initialisiert den RDFSerialiser mit einer knowledgebase, dem namespace und dem namespace-prefix

        Parameters:
        ----------
        knowledgebase: KnowledgeBase
        namespace: string
            TODO: Beschreibung
        namespace_prefix: string
            TODO: Beschreibung

        Returns:
        -------
        None
        """
        self._knowledgebase = knowledgebase
        self._namespace = namespace
        self._namespace_prefix = namespace_prefix
        self._serialisation_format = 'pretty-xml'
        self._graphmanager = GraphManager(self._namespace_prefix, self._namespace)
        super().__init__()

    @abstractmethod
    def serialise_knowledgebase(self, output_path) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_serialisation_format(self, serialisation_format):
        raise NotImplementedError


