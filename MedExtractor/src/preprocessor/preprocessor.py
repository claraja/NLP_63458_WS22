from src.interfaces.interfaces import PreprocessingInterface
from string import punctuation
import re

class RuleBasedPreprocessor(PreprocessingInterface):
    def get_preprocessed_text(self) -> str:
        #nlp = spacy.blank('en')
        # add as a spacy pipeline component
        #nlp.add_pipe('sbd', first=True)  # diese Variable nlp wird noch nicht weiter genutzt 
        with open(self.doc_name, 'r',encoding='unicode_escape') as file:
            raw_text = file.read()

        enumeration = ''
        new_raw_text = ''
        for line in raw_text.split('\n'):
            # delete trailing whitespace
            stripped_line = line.rstrip()
            # ignore empty lines
            if stripped_line == '':
                if (enumeration!='') and (enumeration[-1]!='_'): # siehe z.B. text_10, enumeration_with_space_and_no_punctuation
                    enumeration = f'{enumeration}_'
                elif (enumeration!='') and (enumeration[-1]=='_'):
                    enumeration = ''
                continue
            # ignore normal sentences
            elif stripped_line[-1] == '.':
                pass
            # remember start of enumeration
            elif stripped_line[-1] == ':':
                enumeration = stripped_line[0:-1]
                continue
            # combine start of enumeration with enumerated text
            elif enumeration != '':  
                if (' â€“ ' in stripped_line) & (enumeration!=' '):  # ' â€“ ' entspricht verlängertem Bindestrich, siehe z.B. TextToAnalyze
                    while (stripped_line[0] in punctuation) | (stripped_line[0] == ' '):
                        stripped_line = stripped_line[1:]
                    stripped_line = f"{enumeration}.\n{stripped_line.replace(' â€“ ', ' ')}"
                    enumeration = ' '
                elif (' â€“ ' in stripped_line) & (enumeration==' '):
                    while (stripped_line[0] in punctuation) | (stripped_line[0] == ' '):
                        stripped_line = stripped_line[1:]
                    stripped_line = f"{stripped_line.replace(' â€“ ', ' ')}"
                elif (stripped_line[0] in punctuation) | (stripped_line[0] == ' '):
                    while (stripped_line[0] in punctuation) | (stripped_line[0] == ' '):
                        stripped_line = stripped_line[1:]
                    stripped_line = enumeration + ' ' + stripped_line.replace(' â€“ ', ' ')
                elif (enumeration[-1]=='_'): # siehe z.B. text_10, enumeration_with_space_and_no_punctuation
                    stripped_line = enumeration[:-1] + ' ' + stripped_line.replace(' â€“ ', ' ')
                else:
                    enumeration = ''

            # replace all occurrences of multiple spaces with a single space
            result = re.sub(' +', ' ', stripped_line)
            new_raw_text += f'{result}.\n'
            # further replacements
            new_raw_text = new_raw_text\
                .replace('â€“', ' ')\
                .replace('â€”', ' ')\
                .replace('..', '.')\
                .replace('?.', '?')\
                .replace('!.', '!')\
                .replace('\n ', '\n')
            # replace all occurrences of multiple spaces with a single space
            result = re.sub(' +', ' ', stripped_line)

        return new_raw_text

    """
    @Language.component('sbd')
    def pysbd_sentence_boundaries(self, doc):
        seg = pysbd.Segmenter(language='en', clean=False, char_span=True)
        sents_char_spans = seg.segment(doc.text)
        char_spans = [doc.char_span(sent_span.start, sent_span.end, alignment_mode='contract') for sent_span in sents_char_spans]
        start_token_ids = [span[0].idx for span in char_spans if span is not None]
        for token in doc:
            token.is_sent_start = True if token.idx in start_token_ids else False
        return doc
    """