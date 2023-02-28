from preprocessor import RuleBasedPreprocessor
from preprocessor_ohne_pysbd import RuleBasedPreprocessor_without_pysbd
import glob
import spacy

filenames = [filename for filename in glob.glob("resources/to_analyze" + "/*.txt")]
#filenames = [filename for filename in glob.glob("resources/to_analyze" + "/Claustrophobia.txt")]
number_of_files = len(filenames)
same_sentence_separation = 0

for filename in filenames:
    preprocessor_without = RuleBasedPreprocessor(filename, with_pysbd=False)
    preprocessed_text_without = preprocessor_without.get_preprocessed_text() 
    preprocessor_with = RuleBasedPreprocessor(filename, with_pysbd=True)
    preprocessed_text_with = preprocessor_with.get_preprocessed_text() 
    nlp = spacy.load('en_core_web_sm')

    texts_without_list = [sent.text.rstrip().rstrip('\n').rstrip('\n.').replace('\n', '') for sent in nlp(preprocessed_text_without).sents]
    texts_with_list = [sent.text.rstrip().rstrip('\n').rstrip('\n.').replace('\n', '') for sent in nlp(preprocessed_text_with).sents]

    #print(texts_with_list)
    
    print(filename, '\n')
    print(f'Anzahl gefundener Sätze ist gleich: {len(texts_without_list)==len(texts_with_list)}')
    print(f'Alle Sätze sind gleich: {texts_without_list==texts_with_list}\n')
    if (len(texts_without_list)==len(texts_with_list)) and (texts_without_list==texts_with_list):
        same_sentence_separation += 1

    if texts_without_list!=texts_with_list:
        print(f'ohne pysbd: ')
        for sentence in [x for x in texts_without_list if x not in texts_with_list]:
            print('- ', [sentence])
        print(f'\nmit pysbd: ')
        for sentence in [x for x in texts_with_list if x not in texts_without_list]:
            print('- ', [sentence])

    print('\n==================================================================================\n')
    
print(f'Anzahl Dokumente: {number_of_files}\nAnteil gleich verarbeiteter Dokumente: {same_sentence_separation/number_of_files}')