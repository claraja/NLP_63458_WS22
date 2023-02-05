import csv
import glob
import os
import pickle
import time
import spacy
from tqdm import tqdm
from config_manager import ConfigManager
from interfaces.interfaces import KnowledgeExtractorInterface
from knowledge.base import KnowledgeBase
from knowledge.entity import Entity
from knowledge.entity import EntityType
from knowledge.relations import RelationType
from knowledge.semantics import SemanticRelation
from preprocessor.preprocessor import RuleBasedPreprocessor


class KnowledgeExtractor(KnowledgeExtractorInterface):
    """KnowledgeExtractor searches a text string for entities and for relations between these entities"""

    def __init__(self, config: ConfigManager):
        """Upon initialization of the KnowledgeExtractor data in config.json
        is parsed into attributes of the KnowledgeExtractor instance. An instance
        _nlp of the Language class of spaCy and an instance _kb of the KnowledgeBase
        class are created"""
        print('Starting training of Entity Ruler')
        time_tmp = time.time()                                                          # time stamp
        self._config = config
        self._nlp = spacy.load('en_core_web_sm')                                        # Instantiate spacy.Language object (spaCy pipeline)
        self._doc = self._nlp("")                                                       # Initialize spacy.doc object with empty string
        self._kb = KnowledgeBase()                                                      # Instantiate KnowledgeBase object
        self.context = set()                                                           # Context of a string can be described by adding entities to self.context

        if (self._config.knowledgebase_filename != "") and os.path.exists(self._config.knowledgebase_filename):
            if not config.overwrite:
                self._kb.load(self._config.knowledgebase_filename)

        pipe_exceptions = ['tok2vec','tagger','parser']
        not_required_pipes = [pipe for pipe in self._nlp.pipe_names if pipe not in pipe_exceptions]
        self._nlp.disable_pipes(*not_required_pipes)     # Set up spaCy pipeline

        # spaCy's Entity Ruler is used instead of its Entity Recognizer because the Entity Ruler is easy to 
        # train and shows robust performance. The Entity Recognizer uses a statistical model and requires
        # a large number of medical training sentences which are not available it this point.
        
        self._ruler = self._nlp.add_pipe("entity_ruler")

        # Open the diseases vocabulary
        input_data_file = open(config.diseases_filename, 'r', encoding = "utf-8", errors = 'ignore')
        reader = csv.reader(input_data_file, delimiter='\t')

        training_data = []

        for row in reader:
            to_train = {"label": "DISEASE", "pattern": row[1]}
            training_data.append(to_train)
        input_data_file.close()

        # Open the symptoms vocabulary
        input_data_file = open(config.symptoms_filename, 'r', encoding = "utf-8", errors = 'ignore')
        reader = csv.reader(input_data_file, delimiter='\t')

        for row in reader:
            to_train = {"label": "SYMPTOM", "pattern": row[1]}
            training_data.append(to_train)
        input_data_file.close()
        # Training of Entity Ruler
        # adding training_samples to chunked list to use as tqdm progress bar iterator
        chunk_size = 1000
        list_chunked = [training_data[i:i + chunk_size] for i in range(0, len(training_data), chunk_size)]
        for i in tqdm(range(0, len(list_chunked)), total=len(list_chunked),
                      desc="Training Entity Ruler..."):
            self._ruler.add_patterns(list_chunked[i])
        # self._ruler.add_patterns(training_data)
        print(f'time train Entity Ruler: {time.time() - time_tmp}s')


    def __call__(self,text):
        """KnowledgeExtractor is callable. Input parameter is a text string. This function
        adds all new entity relations it finds in the text string to the database. It also
        adds sentences that prove the relation to the instance of the relation they prove.

        Parameters
        ----------
        text : string
            The text string to be analyzed by the KnowledgeExtractor

        Returns
        -------
        None
        """
        self._doc = self._nlp(text)         # uses spaCy pipeline (w/o pysbd) to analyze the text

        for sent in self._doc.sents:        # Iterates over all sentences (spacy.Span instances)
            sent_text = sent.text           # Saves actual string in sent_text
            entities = set()                # Set (= no dublicates) to collect all entities (symptoms and diseases) found by the entity ruler

            for ent in sent.ents:           # iterates over all entities (spacy.Spans)  found by the entity ruler
                entities.add(ent)
            
            entities.update(self.context)  # updates set of entities with set of entities describing the context
            entities = list(entities)       # converts set to list
            
            for ent1 in entities:           # ent1 and ent2 iterate over all pairs of entities
                for ent2 in entities:
                    relation_type = self.is_related(ent1, ent2, sent)
                    if relation_type != RelationType.NO_RELATION:
                        if relation_type == RelationType.HAS_SYMPTOM:                   # Use of RelationType.IS_SYMPTOM_OF is not yet implemented
                            entity1 = Entity(ent1.text, EntityType.DISEASE)
                            
                            if 'no ' + ent2.text in sent_text:                          # vocabulary does not include negated symptoms. Therefore, the
                                                                                        # text is checked for simple negation of the found symptom
                                entity2 = Entity('no ' + ent2.text, EntityType.SYMPTOM) # if negated, 'no ' is added to the symptom, when instantiating an Entity object
                            else:
                                entity2 = Entity(ent2.text, EntityType.SYMPTOM)

                        relation = SemanticRelation(entity1, entity2, relation_type)    # Instantiation of SematicRelation object with both found entities
                        if not self._kb.has_relation(relation):                         # Check if knowledge base already contains the relation
                            relation.training_samples.append(sent_text.strip('\n'))     # Add sentence to relation object
                            self._kb.add_relation(relation)                             # Add relation to knowledge base
                            if entity1.entity_name not in self._kb._entities:
                                self._kb._entities.append(entity1.entity_name)          # Adds disease to entity list of knowledge base
                            if entity2.entity_name not in self._kb._aliases:
                                self._kb._aliases.append(entity2.entity_name)       	# Add symptom to alias list of knowledge base
                        else:
                            self._kb.add_training_example_to_relation(relation, sent_text)  # If semantic relation is already in knowledge base, only the sentence is
                                                                                            # stored to the semantic relation instance in the knowledge base, if not
                                                                                            # yet contained.

    def set_context(self, context):
        """This function allows defining a context. The context is described by
        named entities included in the Entity Ruler (self._ruler). These entities will
        be added to the set of entities when searching for disease/symptom relations
        between entities.

        Parameters
        ----------
        context : {} (set of spacy.Spans = Entities of Entity Ruler)

        Returns
        -------
        None
        """
        self.context = context
        return

    def get_knowledge_base(self):
        """Returns the knowledgebase that contains all entities and
        sample sentences. Samples sentences can be used for training
        statistical models (e.g. Entity Linker)

        Parameters
        ----------
        None

        Returns
        -------
        KnowledgeBase

        """
        return self._kb
    
    def is_related(self,entity1,entity2,sent):
        """Returns relation type of entity1 and entity2. If both entities are
        found to be unrelated, RelationType.NO_RELATION is returned.

        Parameter sent is not used because this function currently only implements a
        very simple relation check without analyzing the syntax of the sentence. Such
        analysis could be added at a later stage.

        At the moment is_related() just checks whether entity1 is a disease and whether
        entity2 is a symptom. Thus possible results are only RelationType.NO_RELATION
        and RelationType.HAS_SYMPTOM.
        
        Parameters
        ----------
        entity1 : spacy.Span
        entity2 : spacy.Span
        sent : spacy.Span

        Returns
        -------
        RelationType (Enum)
        """
        relation_type = RelationType.NO_RELATION

        if entity1.label_ == "DISEASE" and entity2.label_ == "SYMPTOM":
            relation_type = RelationType.HAS_SYMPTOM
        
        return relation_type
    
    def saveKB(self,*args):
        """Saves the database persistently. Optionally, path and file name are given
        as a string parameter when calling this function. If no path and file name
        are given, the function will use the path and file name in attribute
        self._config.knowledgebase_filename.

        Parameters
        ----------
        file_name : string optional

        Returns
        -------
        None
        """
        error = True
        if len(args) == 0:
            self._kb.save(self._config.knowledgebase_filename)
            error = False 
        elif len(args) == 1:
            if isinstance(args[0],str):
                self._config.knowledgebase_filename = args[0]
                self._kb.save(self._config.knowledgebase_filename)
                error = False
        if error == True:
            print("Fehlerhafte Argumente beim Speichern der Wissensbasis")  # Fehlerhandling muss noch implementiert werden
        return

    def analyze_linguistically(self, text):
        """Method that finds entities in a given text and outputs them on the command line
        together with part-of-speech tags and the syntactic dependency within the sentence

        Parameters
        ----------
        text: string
            The text string to be analyzed by the method

        Returns
        --------
        None
        """
        self._doc = self._nlp(text)

        for sent in self._doc.sents:
            for ent in sent.ents:
                print(ent.text, ent.start_char, ent.end_char, ent.label_)
                for token in self._nlp(self._doc.text[ent.start_char:ent.end_char]):
                    print(token.text, token.tag_, token.dep_)
                print()


    def export_for_entity_linker(self):
        """Exports all entities, aliases and example sentences into an xml-File. The data
        is prepared for easy import into spaCy's Entity Linker. The xml-File is human
        readable and allows reviewing the data that will be used by the Entity Linker.
        Path and filename are defined in config.json.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print(f"size of knowledgebase:  {len(self._kb)}")               # Number of relations saved in knowledge base _kb
        self._kb.export_for_entity_linker(self._config.entity_linker_export_filename)  

    def process_texts(self):
        """Analyzes all text documents in the folder specified in config.json

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        time_tmp = time.time()                                          # time stamp
        # adding filenames to a list for use as tqdm progress bar iterator
        filenames = [filename for filename in glob.glob(self._config.text_folder_name + "/*.txt")]
        for i in tqdm(range(0, len(filenames)), total=len(filenames), desc="Processing files..."):
        # for filename in glob.glob(self._config.text_folder_name + "/*.txt"):   # only .txt files are analyzed
            preprocessor = RuleBasedPreprocessor(filenames[i])
            preprocessed_text = preprocessor.get_preprocessed_text()    # pre-process text file before passing it to knowledge_extractor

            for sent in self._nlp(preprocessed_text).sents:             # uses spaCy pipeline (w/o pysbd) ...
                self(sent.text)                                         # ... to pass only sentences to knowledge_extractor
        
        print(f'time complete loop over files: {time.time() - time_tmp}s') # total time needed for text analysis (does not include training of Entity Ruler)
