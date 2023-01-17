from src.interfaces.interfaces import PreprocessingInterface
import re
import pysbd
import spacy
from spacy import Language
from string import punctuation

class RuleBasedPreprocessor(PreprocessingInterface):
    @Language.component('sbd')
    def pysbd_sentence_boundaries(doc):
        seg = pysbd.Segmenter(language='en', clean=False, char_span=True)
        sents_char_spans = seg.segment(doc.text)
        char_spans = [doc.char_span(sent_span.start, sent_span.end, alignment_mode='contract') for sent_span in sents_char_spans]
        start_token_ids = [span[0].idx for span in char_spans if span is not None]
        for token in doc:
            token.is_sent_start = True if token.idx in start_token_ids else False
        return doc


    def get_preprocessed_text(self) -> str:
        # TODO: funktioniert noch nicht gut z.B. für DrugDependence.txt
        nlp = spacy.blank('en')
        nlp.add_pipe('sbd', first=True) 
        
        our_punctuation = punctuation+' •–'

        with open(self.doc_name, 'r', encoding='utf-8') as file:  
            raw_text = file.read()

        doc = nlp(raw_text)

        enumeration = ''
        new_raw_text = ''
        bullet_point = ''
        for sent_id, sent in enumerate(doc.sents, start=1):
            sentence = sent.text
            # delete trailing whitespace
            stripped_line = sentence.rstrip()
            #print(sent_id, stripped_line, sep='\t|\t')
            # ignore empty lines
            if (stripped_line==''):
                #print(1)
                pass
            # remember start of enumeration
            elif stripped_line[-1] == ':':
                #print(2)
                enumeration = stripped_line[0:-1]
                continue
            elif ((stripped_line[-1] not in ['.', '!', '?', ':']) 
                    and (enumeration=='')):
                #print(3)
                enumeration = stripped_line
                continue
            elif ((stripped_line[-1] not in ['.', '!', '?', ':']) 
                    and (enumeration!='')):
                #print(4)
                stripped_line = stripped_line.lstrip()
                # wenn bullet_point exists sollte er bei allen Teilen 
                # der Aufzählung gleich sein
                if bullet_point!='':
                    if stripped_line.startswith(bullet_point):
                        stripped_line = enumeration + ' ' + stripped_line
                    else:
                        enumeration, bullet_point = '', ''
                else:
                    if stripped_line[0] in our_punctuation:
                        # stripped_line_tmp wird eingeführt um 
                        # Aufzählungszeichen herauszubekommen
                        stripped_line_tmp = stripped_line
                        while (stripped_line_tmp[0] in our_punctuation) | (stripped_line_tmp[0] == ' '):
                            stripped_line_tmp = stripped_line_tmp[1:]
                        # speichere Aufzählungszeichen falls vorhanden
                        if len(stripped_line)!=len(stripped_line_tmp):
                            bullet_point = stripped_line[:stripped_line.index(stripped_line_tmp)]  
                        stripped_line = stripped_line_tmp

                    # String 'symptom' sollte nicht in Symptom vorhanden sein
                    if 'symptom' in stripped_line:
                        enumeration, bullet_point = '', ''
                    else:
                        stripped_line = enumeration + ' ' + stripped_line
            else:
                #print(6)
                enumeration, bullet_point = '', ''

            # replace all occurrences of multiple spaces with a single space
            result = re.sub(' +', ' ', stripped_line)
            new_raw_text += f'{result}.\n'
            # further replacements
            new_raw_text = new_raw_text\
                .replace('..', '.')\
                .replace('?.', '?')\
                .replace('!.', '!')\
                .replace('\n ', '\n')\
                .replace('_', '')\
                .replace(' - ', ' ')\
                .replace(' – ', ' ')
            # replace all occurrences of multiple spaces with a single space
            new_raw_text = re.sub(' +', ' ', new_raw_text)
        
        return new_raw_text
        #return None