from interfaces.interfaces import PreprocessingInterface
import pysbd
import spacy
from spacy.language import Language
from string import punctuation
import re

class RuleBasedPreprocessor(PreprocessingInterface):
    def get_preprocessed_text(self) -> str:
        nlp = spacy.blank('en')
        # add as a spacy pipeline component
        nlp.add_pipe("sbd", first=True)
        with open(self.doc_name, "r") as file:
            raw_text = file.read().replace("\n\n", "\n")

        enumeration = ""
        new_raw_text = ""
        for line in raw_text.split('\n'):
            # ignore empty lines
            if line == "":
                continue
            # delete trailing whitespace
            stripped_line = line.rstrip()
            # ignore normal sentences
            if stripped_line[-1] == '.':
                pass
            # remember start of enumeration
            if stripped_line[-1] == ':':
                enumeration = stripped_line[0:-1]
                continue
            # combine start of enumeration with enumerated text
            elif enumeration != "":
                if stripped_line[0] in punctuation or stripped_line[0] == " ":
                    stripped_line = enumeration + stripped_line[1:]
                else:
                    enumeration = ""

            # replace all occurrences of multiple spaces with a single space
            result = re.sub(' +', ' ', stripped_line)
            new_raw_text = new_raw_text + result + "\n"

        return new_raw_text

    @Language.component("sbd")
    def pysbd_sentence_boundaries(self, doc):
        seg = pysbd.Segmenter(language="en", clean=False, char_span=True)
        sents_char_spans = seg.segment(doc.text)
        char_spans = [doc.char_span(sent_span.start, sent_span.end, alignment_mode="contract") for sent_span in sents_char_spans]
        start_token_ids = [span[0].idx for span in char_spans if span is not None]
        for token in doc:
            token.is_sent_start = True if token.idx in start_token_ids else False
        return doc