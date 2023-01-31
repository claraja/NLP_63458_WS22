from interfaces.interfaces import PreprocessingInterface
import re
import pysbd
import spacy
from spacy import Language
from string import punctuation


class RuleBasedPreprocessor(PreprocessingInterface):
    @Language.component('sbd')
    def pysbd_sentence_boundaries(doc):
        """TODO:Beschreibung

        Parameters:
        ----------
        doc: TODO:dtype
            TODO:Beschreibung

        Returns:
        -------
        TODO:dtype
        """
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
        """Reads the text given in the document with which the Preprocessor is initialised and 
        processes this text such that it is in a good format for further processing.

        Parameters:
        ----------
        None

        Returns:
        -------
        string
        """
        nlp = spacy.blank('en')
        nlp.add_pipe('sbd', first=True)

        our_punctuation = punctuation+' •–-'
        with open(self.doc_name, 'r', encoding='utf-8') as file:
            raw_text = file.read()

        # Aufzählungen sollen als einzelne Sätze gefunden werden
        raw_text = raw_text.replace('•', '\n-')
        # eckige Klammern mit Ziffern (z.B. bei Literaturangaben) entfernen
        raw_text = re.sub('\[\d+\]', '', raw_text)

        doc = nlp(raw_text)

        enumeration, new_raw_text, bullet_point = '', '', ''
        for _, sent in enumerate(doc.sents, start=1):
            sentence = sent.text
            # delete trailing whitespace
            sentence = sentence.rstrip()
            # ignore empty lines
            if (sentence == ''):
                pass
            # remember start of enumeration
            elif sentence[-1] in [':', '—']:
                enumeration = sentence[0:-1]
                continue
            elif ((sentence[-1] not in ['.', '!', '?', ':'])
                    and (enumeration == '')):
                enumeration = sentence
                continue
            elif ((sentence[-1] not in ['.', '!', '?', ':'])
                    and (enumeration != '')):
                sentence = sentence.lstrip()
                # wenn bullet_point existiert sollte er bei allen Teilen
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

                        while ((sentence_tmp[0] in our_punctuation) | (sentence_tmp[0] == ' ')):
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
            processed_sentence = re.sub(' +', ' ', sentence)
            new_raw_text += f'{processed_sentence}.\n'
        # further replacements
        new_raw_text = new_raw_text\
            .replace('..', '.')\
            .replace('?.', '?')\
            .replace('!.', '!')\
            .replace('\n ', '\n')\
            .replace('_', '')\
            .replace('-', ' ')\
            .replace('–', ' ')
        # replace again possible occurrences of multiple spaces with a single space
        new_raw_text = re.sub(' +', ' ', new_raw_text)
        return new_raw_text
