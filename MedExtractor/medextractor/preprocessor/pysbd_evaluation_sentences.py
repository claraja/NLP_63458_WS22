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
doc_name = filenames[6]
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

    for sent in doc_nopysbd.sents:
        sentence = sent.text
        nopysbd_list.append(sentence)


    for _, sent in enumerate(doc_pysbd.sents, start=1):
        sentence = sent.text
        pysbd_list.append(sentence)

    """
    # etwas Verarbeitung:
    # Zeilenumbrüche ('\n') aus Satzanfängen und -enden entfernen
    for i in range(len(nopysbd_list)):
        nopysbd_list[i] = nopysbd_list[i].rstrip('\n').lstrip('\n')
    for i in range(len(pysbd_list)):
        pysbd_list[i] = pysbd_list[i].rstrip('\n').lstrip('\n')

    # Leerzeichen vor und nach Satz entfernen
    nopysbd_list = [x.rstrip().lstrip() for x in nopysbd_list]
    pysbd_list = [x.rstrip().lstrip() for x in pysbd_list]

    # leere Sätze entfernen
    while '' in nopysbd_list:
        nopysbd_list.remove('')
    while '' in pysbd_list:
        pysbd_list.remove('')
    """
    if nopysbd_list!=pysbd_list:
        print(f'ohne pysbd: ')
        for sentence in [x for x in nopysbd_list if x not in pysbd_list]:
            print('- ', [sentence])
        print(f'\nmit pysbd: ')
        for sentence in [x for x in pysbd_list if x not in nopysbd_list]:
            print('- ', [sentence])
    else: 
        print('same sentence separation')

    print('\n==================================================================================\n')
