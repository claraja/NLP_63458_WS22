import csv
import glob
import os
import pickle
import time
import spacy
from src.config_manager import ConfigManager
from src.interfaces.interfaces import KnowledgeExtractorInterface
from src.knowledge.base import KnowledgeBase
from src.knowledge.entity import Entity
from src.knowledge.entity import EntityType
from src.knowledge.relations import RelationType
from src.knowledge.semantics import SemanticRelation
from src.preprocessor.preprocessor import RuleBasedPreprocessor


class KnowledgeExtractor(KnowledgeExtractorInterface):
    """KnowledgeExtractor searches a text string for entities and for relations between these entities"""

    def __init__(self, config: ConfigManager):
        """Upon initialization of the KnowledgeExtractor data in config.json
        is parsed into attributes of the KnowledgeExtractor instance. An instance
        _nlp of the Language class of spaCy and an instance _kb of the KnowledgeBase
        class are created"""

        time_tmp = time.time()
        self._knowledgebase_filename = config.knowledgebase_filename
        self._text_folder_name = config.text_folder_name
        self._entity_linker_export_filename = config.entity_linker_export_filename
        self._nlp = spacy.load('en_core_web_sm')
        self._doc = self._nlp("")
        self._kb = KnowledgeBase()
        self._context = []

        if (self._knowledgebase_filename != "") and os.path.exists(self._knowledgebase_filename):
            if not config.overwrite:
                self._kb.load(self._knowledgebase_filename)

        pipe_exceptions = ['tok2vec','tagger','parser']
        not_required_pipes = [pipe for pipe in self._nlp.pipe_names if pipe not in pipe_exceptions]
        self._nlp.disable_pipes(*not_required_pipes)

        self._ruler = self._nlp.add_pipe("entity_ruler")

        input_data_file = open(config.diseases_filename, 'r', encoding = "utf-8", errors = 'ignore')

        reader = csv.reader(input_data_file, delimiter='\t')

        training_data = []

        for row in reader:
            to_train = {"label": "DISEASE", "pattern": row[1]}
            training_data.append(to_train)
        input_data_file.close()

        self._ruler.add_patterns(training_data)

        input_data_file = open(config.symptoms_filename, 'r', encoding = "utf-8", errors = 'ignore')

        reader = csv.reader(input_data_file, delimiter='\t')

        for row in reader:
            to_train = {"label": "SYMPTOM", "pattern": row[1]}
            training_data.append(to_train)
        input_data_file.close()
        self._ruler.add_patterns(training_data)
        # self._nlp.add_pipe("negex")
        print(f'time create knowledgeExtractor: {time.time() - time_tmp}s')


    def __call__(self,text):
        """KnowledgeExtractor is callable. Input parameter is a text string. This function
        adds all new entity relations it finds in the text string to the database.

        Parameters:
        ----------
        text: string
            The text string to be analyzed by the KnowledgeExtractor

        Returns:
        -------
        None
        """
        self._doc = self._nlp(text)

        for sent in self._doc.sents:
            sent_text = sent.text
            entities = set()

            for ent in sent.ents:
                entities.add(ent)
            entities = list(entities)
            entities += self._context

            for ent1 in entities:
                for ent2 in entities:
                    res = self._is_related(ent1, ent2, sent)
                    if res != RelationType.NO_RELATION:
                        if (ent1.label_ == "DISEASE" and ent2.label_ == "SYMPTOM"):
                            entity1 = Entity(ent1.text,EntityType.DISEASE)
                            
                            if 'no ' + ent2.text not in sent_text:
                                entity2 = Entity(ent2.text,EntityType.SYMPTOM)
                            else:
                                entity2 = Entity('no ' + ent2.text,EntityType.SYMPTOM)

                        relation = SemanticRelation(entity1, entity2, res)
                        if not self._kb.has_relation(relation):
                            relation.training_samples.append(sent_text.strip('\n'))
                            self._kb.add_relation(relation)
                            if entity1.entity_name not in self._kb._entities:
                                self._kb._entities.append(entity1.entity_name)
                            if entity2.entity_name not in self._kb._aliases:
                                self._kb._aliases.append(entity2.entity_name)
                        else:
                            self._kb.add_training_example_to_relation(relation, sent_text)
                            # relation = self._kb.give_relation(relation)
                            # if sent_text.strip('\n') not in relation.training_samples:
                            #     relation.training_samples.append(sent_text.strip('\n'))

    def set_context(self, context):
        """This function allows to define a context. The context is described by a
        named entity included in the Entity Ruler (self._ruler). This entity will
        be added to the list of entities when searching for disease/symptom relations
        between entities.

        Parameters:
        ----------
        context: Span

        Returns:
        -------
        None
        """
        self._context = context
        return

    def get_knowledge_base(self):
        """Returns the knowledgebase that contains all entities (including aliases)
        and sample sentences that can be used for training statistical models

        Parameters:
        ----------
        None

        Returns:
        ------
        KnowledgeBase

        """

        return self._kb
    
    def _is_related(self,entity1,entity2,sent):

        relation = RelationType.NO_RELATION

        if entity1.label_ == "DISEASE" and entity2.label_ == "SYMPTOM":
            relation = RelationType.HAS_SYMPTOM
        
        return relation
    
    def saveKB(self,*args):
        """Saves the database persistently. Optionally, path and file name are given
        as a string parameter when calling this function. If no path and file name
        are given, the function will use the path and file name in attribute
        self._knowledgebase_filename.

        Parameters:
        ----------
        (optional) file_name (string)

        Returns:
        -------
        None
        """
        error = True
        if len(args) == 0:
            self._kb.save(self._knowledgebase_filename)
            error = False 
        elif len(args) == 1:
            if isinstance(args[0],str):
                self._knowledgebase_filename = args[0]
                self._kb.save(self._knowledgebase_filename)
                error = False
        if error == True:
            print("Fehlerhafte Argumente beim Speichern der Wissensbasis")  # Fehlerhandling muss noch implementiert werden
        return

    def call2(self,text):

        self._doc = self._nlp(text)

        # displacy.serve(self._doc, style="ent")
        for sent in self._doc.sents:
            entities = []

            for ent in sent.ents:
                print(ent.text, ent.start_char, ent.end_char, ent.label_)
                # print(self._doc.text[ent.start_char:ent.end_char])
                for token in self._nlp(self._doc.text[ent.start_char:ent.end_char]):
                    print(token.text, token.tag_, token.dep_)
                print()

            print("------")

    def export_for_entity_linker(self):
        """Exports all entities, aliases and example sentences into an xml-File. The data
        is prepared for easy import into spaCy's Entity Linker. The xml-File is human
        readable and allows reviewing the data that will be used by the Entity Linker.
        Path and filename are defined in config.json.

        Parameters:
        ----------
        None

        Returns:
        --------
        None
        """
        print(f"size of knowledgebase:  {len(self._kb)}")
        self._kb.export_for_entity_linker(self._entity_linker_export_filename)

    def process_texts(self):
        """Analyzes all text documents in the folder specified in config.json

        Parameters:
        ----------
        None

        Returns:
        -------
        None
        """
        time_tmp = time.time()
        for filename in glob.glob(self._text_folder_name + "/*.txt"):
            preprocessor = RuleBasedPreprocessor(filename)
            preprocessed_text = preprocessor.get_preprocessed_text()

            for sent in self._nlp(preprocessed_text).sents:
                self(sent.text)
        print(f'time complete loop over files: {time.time() - time_tmp}s')

