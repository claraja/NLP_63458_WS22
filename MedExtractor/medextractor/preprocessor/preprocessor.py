from interfaces.interfaces import PreprocessingInterface
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
        char_spans = [doc.char_span(sent_span.start, sent_span.end,
                                    alignment_mode='contract') for sent_span in sents_char_spans]
        start_token_ids = [
            span[0].idx for span in char_spans if span is not None]
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

        enumeration, new_raw_text, bullet_point = '', '', ''
        for sent_id, sent in enumerate(doc.sents, start=1):
            sentence = sent.text
            # delete trailing whitespace
            sentence = sentence.rstrip()
            # print(sent_id, sentence, sep='\t|\t')
            # ignore empty lines
            if (sentence == ''):
                pass
            # remember start of enumeration
            elif sentence[-1] == ':':
                enumeration = sentence[0:-1]
                continue
            elif ((sentence[-1] not in ['.', '!', '?', ':'])
                    and (enumeration == '')):
                enumeration = sentence
                continue
            elif ((sentence[-1] not in ['.', '!', '?', ':'])
                    and (enumeration != '')):
                sentence = sentence.lstrip()
                # wenn bullet_point exists sollte er bei allen Teilen
                # der Aufzählung gleich sein
                if bullet_point != '':
                    if sentence.startswith(bullet_point):
                        sentence = enumeration + ' ' + sentence
                    else:
                        enumeration, bullet_point = '', ''
                else:
                    if sentence[0] in our_punctuation:
                        # sentence_tmp wird eingeführt um
                        # Aufzählungszeichen herauszubekommen
                        sentence_tmp = sentence

                        # In der While-Schleife wurde die Bedingung   sentence_tmp != ''   ergänzt.
                        # Grund: pyspd scheint Probleme mit den Literaturangaben wie z.B. '[1]' zu haben.
                        # Es kommt vor, dass die schließende Klammer nicht mehr als Teil des Satzes gesehen wird.
                        # Dann wird aus ']' ein einzelner Satz. Wird dann das Zeichen ']' entfernt, ist der
                        # verbleibende String leer. Alternativ könnte man alle Literaturangaben aus
                        # dem Text entfernen, bevor spaCy zum Einsatz kommt.
                        while (sentence_tmp != '') and ((sentence_tmp[0] in our_punctuation) | (sentence_tmp[0] == ' ')):
                            sentence_tmp = sentence_tmp[1:]
                        # speichere Aufzählungszeichen falls vorhanden
                        if len(sentence) != len(sentence_tmp):
                            bullet_point = sentence[:sentence.index(
                                sentence_tmp)]
                        sentence = sentence_tmp
                    # String 'symptom' sollte nicht in Symptom vorhanden sein
                    if 'symptom' in sentence:
                        enumeration, bullet_point = '', ''
                    else:
                        sentence = enumeration + ' ' + sentence
            else:
                enumeration, bullet_point = '', ''
            # replace all occurrences of multiple spaces with a single space
            result = re.sub(' +', ' ', sentence)
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
        # replace again possible occurrences of multiple spaces with a single space
        new_raw_text = re.sub(' +', ' ', new_raw_text)
        return new_raw_text
