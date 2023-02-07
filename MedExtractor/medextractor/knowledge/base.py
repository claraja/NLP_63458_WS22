import xml.etree.ElementTree as ElementTree
from knowledge.semantics import SemanticRelation
from knowledge.entity import Entity
from knowledge.entity import EntityType
import pickle
import spacy


class KnowledgeBase:
    """
        The KnowledgeBase manages entities and relations.

        Functions:
        add_relation(SemanticRelation)
        has_relation(SemanticRelation) -> bool
        give_entities(str) -> []
        export_for_entity_linker(str)
        safe(str)
        load(str)
    """

    def __init__(self):
        self.semantic_relations = []
        self.allow_duplicates = False
        self._entities = []
        self._aliases = []
        self._training_samples = []

    def __len__(self):
        return len(self.semantic_relations)

    def add_relation(self, relation: SemanticRelation) -> None:
        """
        Add a SemanticRelation into the KnowledgeBase.
        
        Parameters
        ----------
        relation: SemanticRelation
        """

        if self.allow_duplicates:
            self.semantic_relations.append(relation)
        else:
            if not self.has_relation(relation):
                self.semantic_relations.append(relation)

    def has_relation(self, relation: SemanticRelation) -> bool:
        """
        Return True if the relation is in the KnowledgeBase. Return False otherwise.

        Parameters
        ----------
        relation: SemanticRelation
        """
        for other in self.semantic_relations:
            if other == relation:
                return True
        return False

    def add_training_example_to_relation(self, relation: SemanticRelation, sent_text: str) -> None:
        """
        Add a training sentence to a SemanticRelation

        Parameters
        ----------
        relation: SemanticRelation
        sent_text: str
            training sentence
        """
        for other in self.semantic_relations:
            if other == relation:
                if sent_text.strip('\n') not in other.training_samples:
                    other.training_samples.append(sent_text.strip('\n'))


    def get_entities(self, alias: str) -> []:
        """
        Return a list of entities that are related to symptoms in SemanticRelations stored in the KnowledgeBase

        Parameters
        ----------
        alias: str
            the name of a symptom

        Returns
        -------
        list of Entity
        """
        alias_entity = Entity(alias, EntityType.SYMPTOM)
        result = []
        for relation in self.semantic_relations:
            if relation.entity_2 == alias_entity:
                result.append(relation.entity_1)
        return result

    def export_for_entity_linker(self, file_name: str):
        """
        Save the KnowledgeBase data as an xml file that can be used to train an entity linker.

        Parameters
        ----------
        file_name: str
            the name of the xml file
        """
        nlp = spacy.load('en_core_web_sm')                  # a new spacy.Language object is instantiated because a new Entity Ruler will be trained
        pipe_exceptions = ['tok2vec', 'tagger', 'parser']
        not_required_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        nlp.disable_pipes(*not_required_pipes)
        ruler = nlp.add_pipe("entity_ruler")                # will be trained only with entities contained in the knowledge base
        ruler_training_data = []

        entity_linker_export = ElementTree.Element("entity_linker_export")      # root of the xml-tree
        
        # Add entities (diseases) to the xml file
        entity_node = ElementTree.SubElement(entity_linker_export, "entities")  # first node is for the collection of named entities (diseases)

        for entity in sorted(self._entities):                                   # iterates over all entities in the knowledge base
            entity_xml = ElementTree.SubElement(entity_node, "entity", {"typ": "str"})  # new element and set </entity> as the tag of the new element
            entity_xml.text = entity                                            # adds the entity to the </entities> branch
            to_train = {"label": "DISEASE", "pattern": entity}
            ruler_training_data.append(to_train)                                # adds the entity to the training samples for the entity ruler

        ruler.add_patterns(ruler_training_data)                                 # trains the entity ruler with diseases

        # Add aliases (symptoms) to the xml file
        alias_node = ElementTree.SubElement(entity_linker_export, "aliases")    # next node is for the collection of aliases (symptoms)
        ruler_training_data = []
        for alias in sorted(self._aliases):                                     # iterates over all aliases (symptoms) in the knowledge base
            
            alias_xml = ElementTree.SubElement(alias_node, "alias", {"typ": "str"}) # new element and set </alias> as the tag of the new element
            alias_xml.text = alias                                              # adds the symptom (alias) to the </aliases> branch

            alias_entity_node = ElementTree.SubElement(alias_xml, "alias_entities")    # for each alias (symptom) all related entities (diseases) will be added
            for relation in self.semantic_relations:                            # iterates over all semantic relations contained in the knowledge base
                if relation.entity_2.entity_name == alias:                      # if the symptom (alias) is part of the semantic relation ...
                    alias_entity_xml = ElementTree.SubElement(alias_entity_node, "alias_entity") 
                    alias_entity_xml.text = relation.entity_1.entity_name       # ... the related disease (entity) will be added with tag </alias_entity>

            to_train = {"label": "SYMPTOM", "pattern": alias}                   # adds the symptoms to the training samples for the entity ruler
            ruler_training_data.append(to_train)

        ruler.add_patterns(ruler_training_data)                                 # trains the entity ruler with symptoms

        # Add training sentences to the xml file
        training_node = ElementTree.SubElement(entity_linker_export, "training")    # New node </training>
        
        for relation in self.semantic_relations:                                # iterate over all semantic relations ... 

            for sample in relation.training_samples:                            # ... and over all sentences saved for the semantic relation instance

                if sample in [string.text for string in list(entity_linker_export.iter("sample"))]:     # avoid dublicates when adding sentences
                    break

                sample_xml = ElementTree.SubElement(training_node, "sample", {"typ": "str"})            # add new sub-node </sample>           
                sample_xml.text = sample                                                                # add sentence

                indices = []

                training_links_node = ElementTree.SubElement(sample_xml, "links")   # new sub-node </links> to define how to link an alias to an entity

                doc = nlp(sample)               # the sentence is process by spaCy pipeline to search for named entities (diseases and symptoms).

                                                # remark: the big vocabulary trained for the knowledge_extractor may contain a symptom 'motivation'. However, the
                                                # actual symptom may be the negated 'no motivation' which is not in the training vocabulary of 
                                                # knowledge_extractor. But knowledge_extractor stores 'no motivation' in the knowledge base. Since we have
                                                # trained the entity ruler only with the entities and aliases contained in the knowledge base, now this
                                                # spaCy pipeline searches for 'no motivation'. This is one of the main reasons to work with a new pipeline.

                for alias in self._aliases:     # iterates over all aliases (symptoms) contained in the knowledge base

                    doc_entities = [ent.text for ent in doc.ents]   # list of all named entities found by the spaCy pipeline

                    if alias in doc_entities:                   # if an alias (symptom) is found in the sentence ...
                        for ent in doc.ents:                    # ... the programm iterates over all found entities (spacy.span's) of the sentence ...
                            if ent.text == alias:               # ... in order to add for ALL appearances of this alias in the sentence ...
                                start = ent.start_char          # ... the start and ...
                                end = start + len(alias)        # ... end position within the sentence.
                                should_add = True               # The alias will only be added if not overlapping with another alias, that was already added
                                for i in indices:
                                    if not ((end < i[0]) or (start > i[1])):
                                        should_add = False
                                        break
                                if should_add == True:
                                    indices.append((start, end))    # append tuple with the start and end positions

                                    training_alias_xml = ElementTree.SubElement(training_links_node, "alias_type",  # add 'SYMPTOM' as </alias_type>
                                                                                {"typ": "str"})
                                    training_alias_xml.text = "SYMPTOM"

                                    training_links_xml = ElementTree.SubElement(training_links_node, "position",    # add position data with </position> tag
                                                                                {"typ": "tuple"})
                                    training_links_xml.text = "(" + str(start) + "," + str(end) + ")"       # add tupel as string (e.g. '(34,40)')

                                    entity_list = self.get_entities(
                                        alias)  # returns all entities (diseases) related to the alias (symptom)
                                    entity_count = 0

                                    for ent in entity_list:                     # count number of diseases that are related to the symptom ...
                                        if ent.entity_name in sample:           # ... AND that are found in the sentence
                                            entity_count += 1

                                    training_entities_node = ElementTree.SubElement(training_links_xml,     # new sub-node for all entities related to the alias, tag </entities_training>
                                                                                    "entities_training")
                                    for ent in entity_list:

                                        training_entities_xml = ElementTree.SubElement(training_entities_node,  # new element </training_entity>
                                                                                       "training_entity",
                                                                                       {"typ": "str"})
                                        training_entities_xml.text = ent.entity_name                            # add entity name

                                        training_probability_node = ElementTree.SubElement(training_entities_xml,   # new sub-node </probability>
                                                                                           "probability")
                                        training_probability_xml = ElementTree.SubElement(training_probability_node,    # value, tag is </prob>
                                                                                          "prob", {"typ": "float"})

                                        if ent.entity_name in sample:                                           # if entity (disease) is mentioned in the sentence ...
                                            training_probability_xml.text = str(round(1.0 / entity_count, 1))   # ... its probability > 0 is added
                                        else:
                                            training_probability_xml.text = "0.0"                               # ... otherwise probability is 0.0

        if file_name != "":                                         
            et = ElementTree.ElementTree(entity_linker_export)
            et.write(file_name, encoding='utf-8')                   # xml file is written to disk

    def save(self, file_name: str) -> None:
        """
        Save the KnowledgeBase into a pickle file.
        If the KnowledgeBase does not contain any SemanticRelations, no file is saved.

        Parameters
        ----------
        file_name: str
            the name of the file
        """
        if len(self.semantic_relations) == 0:
            print("KnowledgeBase is empty. Not saving.")
            return
        if file_name != '':
            with open(file_name, 'wb') as file:
                pickle.dump([self.semantic_relations, self._entities, self._aliases], file)
        else:
            raise NameError

    def load(self, file_name: str):
        """
        Load the KnowledgeBase from file.

        Parameters
        ----------
        file_name: str
            the name of the file
        """
        if file_name == '':
            with open(file_name, 'rb') as file:
                self.semantic_relations, self._entities, self._aliases = pickle.load(file)

