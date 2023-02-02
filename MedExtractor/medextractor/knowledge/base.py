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


    def give_entities(self, alias: str) -> []:
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
        nlp = spacy.load('en_core_web_sm')
        pipe_exceptions = ['tok2vec', 'tagger', 'parser']
        not_required_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        nlp.disable_pipes(*not_required_pipes)
        ruler = nlp.add_pipe("entity_ruler")
        ruler_training_data = []

        entity_linker_export = ElementTree.Element("entity_linker_export")
        entity_node = ElementTree.SubElement(entity_linker_export, "entities")

        for entity in sorted(self._entities):
            entity_xml = ElementTree.SubElement(entity_node, "entity", {"typ": "str"})
            entity_xml.text = entity
            to_train = {"label": "DISEASE", "pattern": entity}
            ruler_training_data.append(to_train)

        ruler.add_patterns(ruler_training_data)

        alias_node = ElementTree.SubElement(entity_linker_export, "aliases")
        ruler_training_data = []
        for alias in sorted(self._aliases):
            to_train = {"label": "SYMPTOM", "pattern": alias}
            ruler_training_data.append(to_train)
            alias_xml = ElementTree.SubElement(alias_node, "alias", {"typ": "str"})
            alias_xml.text = alias

            alias_entity_node = ElementTree.SubElement(alias_xml, "alias_entities")
            for relation in self.semantic_relations:
                if relation.entity_2.entity_name == alias:
                    alias_entity_xml = ElementTree.SubElement(alias_entity_node, "alias_entity")
                    alias_entity_xml.text = relation.entity_1.entity_name

        ruler.add_patterns(ruler_training_data)

        training_node = ElementTree.SubElement(entity_linker_export, "training")

        for relation in self.semantic_relations:

            for sample in relation.training_samples:

                if sample in [string.text for string in list(entity_linker_export.iter("sample"))]:
                    break

                sample_xml = ElementTree.SubElement(training_node, "sample", {"typ": "str"})
                sample_xml.text = sample

                indices = []

                # training_aliases_node = ElementTree.SubElement(sample_xml, "aliases_training")
                training_links_node = ElementTree.SubElement(sample_xml, "links")

                doc = nlp(sample)

                for alias in self._aliases:

                    doc_entities = [ent.text for ent in doc.ents]

                    if alias in doc_entities:
                        for ent in doc.ents:
                            if ent.text == alias:
                                # start = sample.find(alias)
                                start = ent.start_char
                                # end = sample.find(alias) + len(alias)
                                end = start + len(alias)
                                should_add = True
                                for i in indices:
                                    if not ((end < i[0]) or (start > i[1])):
                                        should_add = False
                                        break
                                if should_add == True:
                                    indices.append((start, end))

                                    training_alias_xml = ElementTree.SubElement(training_links_node, "alias_type",
                                                                                {"typ": "str"})
                                    training_alias_xml.text = "SYMPTOM"

                                    training_links_xml = ElementTree.SubElement(training_links_node, "position",
                                                                                {"typ": "tuple"})
                                    training_links_xml.text = "(" + str(start) + "," + str(end) + ")"

                                    entity_list = self.give_entities(alias)
                                    entity_count = 0

                                    for ent in entity_list:
                                        if ent.entity_name in sample:
                                            entity_count += 1

                                    training_entities_node = ElementTree.SubElement(training_links_xml,
                                                                                    "entities_training")
                                    for ent in entity_list:

                                        training_entities_xml = ElementTree.SubElement(training_entities_node,
                                                                                       "training_entity",
                                                                                       {"typ": "str"})
                                        training_entities_xml.text = ent.entity_name

                                        training_probability_node = ElementTree.SubElement(training_entities_xml,
                                                                                           "probability")
                                        training_probability_xml = ElementTree.SubElement(training_probability_node,
                                                                                          "prob", {"typ": "float"})

                                        if ent.entity_name in sample:
                                            training_probability_xml.text = str(round(1.0 / entity_count, 1))
                                        else:
                                            training_probability_xml.text = "0.0"

                # for word in sample.translate(str.maketrans('', '', string.punctuation)).split():
                #    if word.isalpha():
                #        output += ",-1"
                # output += "])"

        if file_name != "":
            et = ElementTree.ElementTree(entity_linker_export)
            et.write(file_name, encoding='utf-8')

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

