import re
import pysbd
import spacy
import glob
from spacy import Language


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


filenames = [filename for filename in glob.glob("resources/to_analyze" + "/*.txt")]
#doc_name = filenames[4]
number_of_files = len(filenames)
same_sentence_separation = 0
with_some_preprocessing = True  # whether some processing should be done after the sentence boundary detection
for doc_name in filenames[:-1]:
    print(f'====================== {doc_name} ==================')

    nlp_pysbd = spacy.blank('en')
    nlp_pysbd.add_pipe('sbd', first=True)

    nlp = spacy.load('en_core_web_sm')

    with open(doc_name, 'r', encoding='utf-8') as file:
        raw_text = file.read()

        pysbd_list = []
        nopysbd_list = []

        doc_pysbd = nlp_pysbd(raw_text)
        doc_nopysbd = nlp(raw_text)

        if with_some_preprocessing:

            # Sätze, die ein \n enthalten, werden an dieser Stelle in zwei Sätze aufgesplittet
            for sent in doc_nopysbd.sents:
                sentence = sent.text
                sentences = sentence.split('\n')
                for sentence in sentences:
                    nopysbd_list.append(sentence)


            for _, sent in enumerate(doc_pysbd.sents, start=1):
                sentence = sent.text
                sentences = sentence.split('\n')
                for sentence in sentences:
                    pysbd_list.append(sentence)

            # Leerzeichen vor und nach Satz werden entfernt
            nopysbd_list = [x.rstrip().lstrip() for x in nopysbd_list]
            pysbd_list = [x.rstrip().lstrip() for x in pysbd_list]

            # leere Sätze werden entfernt
            while '' in nopysbd_list:
                nopysbd_list.remove('')
            while '' in pysbd_list:
                pysbd_list.remove('')
        
        else:
            for sent in doc_nopysbd.sents:
                sentence = sent.text
                nopysbd_list.append(sentence)


            for _, sent in enumerate(doc_pysbd.sents, start=1):
                sentence = sent.text
                pysbd_list.append(sentence)
        
        if nopysbd_list!=pysbd_list:
            print(f'ohne pysbd: ')
            for sentence in [x for x in nopysbd_list if x not in pysbd_list]:
                print('- ', [sentence])
            print(f'\nmit pysbd: ')
            for sentence in [x for x in pysbd_list if x not in nopysbd_list]:
                print('- ', [sentence])
        else: 
            #print('same sentence separation')
            same_sentence_separation += 1
        
        #for sentence in pysbd_list:
        #    print('- ', [sentence])
        
        print('==================================================================================\n')
print(f'Anzahl files: {number_of_files}')
print(f'Anzahl gleichverarbeiteter Texte: {same_sentence_separation}')
print(f'Anteil gleichverarbeiteter Texte: {same_sentence_separation/number_of_files}')
