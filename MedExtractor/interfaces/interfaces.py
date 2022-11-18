from abc import ABC, abstractmethod

class PreprocessingInterface(ABC):

    def __init__(self, doc_name):
        self.doc_name = doc_name
        super().__init__()

    @abstractmethod
    def get_preprocessed_text(self) -> str:
        raise NotImplementedError

class KnowledgeExtractorInterface(ABC):

    def __init__(self, text):
        self.text = text
        super().__init__()

    @abstractmethod
    def get_knowledge_base(self) -> str:
        raise NotImplementedError

class RDFSerialiserInterface(ABC):

    def __init__(self, knowledgebase):
        self.knowledgebase = knowledgebase
        super().__init__()

    @abstractmethod
    def serialise_knowledgebase(self) -> str:
        raise NotImplementedError