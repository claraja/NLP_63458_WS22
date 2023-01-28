import csv
import _pickle as cPickle
import pickle


import spacy
import time
import os
import spacy_transformers
from negspacy.negation import Negex


class RulerCreator:
    def __init__(self):
        self._nlp = spacy.load('en_core_web_sm')
        self._doc = self._nlp("")

        pipe_exceptions = ['tok2vec', 'tagger', 'parser']
        not_required_pipes = [pipe for pipe in self._nlp.pipe_names if pipe not in pipe_exceptions]
        self._nlp.disable_pipes(*not_required_pipes)

        self._ruler = self._nlp.add_pipe("entity_ruler")
        time_tmp = time.time()
        # input_diseases_path = os.path.join('training_diseases.txt')
        # p = os.path.join('resources', 'training_data', 'knowledge_extractor/config.cfg')
        print("cwd: " + os.getcwd())
        input_diseases_path = os.path.join('../resources', 'training_data', 'training_diseases_klein.txt')
        input_data_file = open(input_diseases_path, 'r', encoding="unicode_escape")
        reader = csv.reader(input_data_file, delimiter='\t')

        diseases_training_data = []

        for row in reader:
            to_train = {"label": "DISEASE", "pattern": row[1]}
            diseases_training_data.append(to_train)
        input_data_file.close()
        print(f'time read diseases: {time.time() - time_tmp}s')

        time_tmp = time.time()
        self._ruler.add_patterns(diseases_training_data)
        print(f'time add diseases to ruler: {time.time() - time_tmp}s')

        time_tmp = time.time()
        # input_symptoms_path = os.path.join( 'training_symptoms.txt')
        input_symptoms_path = os.path.join('../resources', 'training_data', 'training_symptoms_klein.txt')
        input_data_file = open(input_symptoms_path, 'r', encoding="unicode_escape")
        reader = csv.reader(input_data_file, delimiter='\t')

        symptoms_training_data = []

        for row in reader:
            to_train = {"label": "SYMPTOM", "pattern": row[1]}
            symptoms_training_data.append(to_train)
        input_data_file.close()
        print(f'time read symptoms: {time.time() - time_tmp}s')

        time_tmp = time.time()
        self._ruler.add_patterns(symptoms_training_data)
        print(f'time add symptoms to ruler: {time.time() - time_tmp}s')
        self._nlp.add_pipe("negex")

    def save(self) -> None:
        config = self._nlp.config
        pipeline_path = os.path.join('../resources', 'pipeline')
        p = os.path.join(pipeline_path, 'config.cfg')
        with open(p, 'wb') as file:
            pickle.dump(config, file)

        bytes_data = self._nlp.to_bytes()
        p = os.path.join(pipeline_path, 'pipeline.bin')
        with open(p, 'wb') as f:
            f.write(bytes_data)

    def load(self):
        time_tmp = time.time()
        pipeline_path = os.path.join('../resources', 'pipeline')
        p = os.path.join(pipeline_path, 'config.cfg')
        with open(p, 'rb') as f:
            config = pickle.load(f)
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        self._nlp = lang_cls.from_config(config)
        print(f'time load config: {time.time() - time_tmp}s')
        time_tmp = time.time()
        p = os.path.join(pipeline_path, 'pipeline.bin')
        with open(p, 'rb') as f:
            bytes_data = f.read()
        self._nlp.from_bytes(bytes_data)
        print(f'time load pipeline: {time.time() - time_tmp}s')


ruler_creator = RulerCreator()
ruler_creator.save()
