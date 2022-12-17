import sys
sys.path.append("D:\Git_Fachpraktikum")
sys.path.append("D:\Git_Fachpraktikum\MedExtractor")
sys.path.append("D:\Git_Fachpraktikum\MedExtractor\interfaces")

from MedExtractor.interfaces.interfaces import KnowledgeExtractorInterface

class KnowledgeExtractor(KnowledgeExtractorInterface):
    def __init__(self,kb_name,nlp):
        super().__init__(kb_name,nlp)
        doc = nlp("")
        pipe_exceptions = ['tagger','parser']
        not_required_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        nlp.disable_pipes(*not_required_pipes)
        ruler = nlp.add_pipe("entity_ruler")
        print(nlp.pipe_names)

    def __call__(text):
        pass

    def set_context(self):
        pass
    
    def get_knowledge_base(self):
        pass
    
    def is_related(self):
        pass