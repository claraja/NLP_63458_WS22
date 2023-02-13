import re
import pysbd
import spacy
from spacy import Language
from string import punctuation


class RuleBasedPreprocessor():

    def __init__(self, doc_name):
        self.doc_name = doc_name

    @Language.component('sbd')
    def pysbd_sentence_boundaries(doc):
        """Creates a SpaCy pipeline component to segment a text into sentences using pysbd.

        Parameters
        ----------
        doc : Doc
            SpaCy Doc object

        Returns
        -------
        doc : Doc
            SpaCy Doc object
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

        Parameters
        ----------
        None

        Returns
        -------
        string
        """
        nlp = spacy.blank('en')
        nlp.add_pipe('sbd', first=True)

        our_punctuation = punctuation+' •–-'
        with open(self.doc_name, 'r', encoding='utf-8') as file:
            raw_text = file.read()

        # enumerations should be found as individual sentences
        raw_text = raw_text.replace('•', '\n-')
        # square brackets with digits in them 
        # (for example in bibliographic references) are removed
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
                # if bullet point exists it should be the 
                # same for all parts of the enumeration
                if bullet_point != '':
                    if sentence.startswith(bullet_point):
                        sentence = enumeration + ' ' + sentence
                    else:
                        enumeration, bullet_point = '', ''
                else:
                    if sentence[0] in our_punctuation:
                        # sentence_tmp is introduced to get 
                        # kind of bullet point if existent
                        sentence_tmp = sentence

                        while (sentence_tmp != '' and (sentence_tmp[0] in our_punctuation) | (sentence_tmp[0] == ' ')):
                            sentence_tmp = sentence_tmp[1:]
                        # save kind of bullet point if existent
                        if len(sentence) != len(sentence_tmp):
                            bullet_point = sentence[:sentence.index(
                                sentence_tmp)]
                        sentence = sentence_tmp
                    # string 'symptom' should not be a part of a symptom
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
