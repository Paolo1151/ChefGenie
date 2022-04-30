from sklearn.feature_extraction.text import TfidfVectorizer
from decouple import config

from .recipe import Recipe
from .filters import SearchConfig

import pandas as pd
import numpy as np


import spacy
import joblib
import os
import psycopg2

class NLPModel:
    def __init__(self, pool_table):
        '''Create an NLP Processor with an internal nlp object for nlp operations'''
        try:
            self.nlp = spacy.load('en_core_web_md')
        except:
            spacy.cli.download('en_core_web_md')
            self.nlp = spacy.load('en_core_web_md')

        print('Initialized NLPModel...')

    def process(self, text):
        '''
        Parameters
        -----------
        text : str
            a text input to be processed

        Returns
        -----------
        processed_text : str
            a processed string object
        '''
        doc = self.nlp(text)
        cleaned_text = ''
        processed_text = ''

        for token in doc:
            if not(token.is_stop or token.is_punct or token.like_num):
                cleaned_text += token.lemma_.lower() + ' '

        cleaned_text = cleaned_text.strip()

        vect = TfidfVectorizer()
        X = vect.fit_transform([cleaned_text])
        df = pd.DataFrame(X.toarray(), columns=vect.get_feature_names_out())\
            .T\
            .sort_values(by=0)\
            .iloc[:min(10, X.shape[1])]

        for val in df.index:
            processed_text += val + ' '
        
        return processed_text

    def compare(self, text1, text2):
        '''
        Attributes:
        -----------
        text1 : str
            The first text for comparison
        
        text2 : str
            The second text for comparison

        Returns:
        -----------
        similarity : float
            The document similarity score of the two texts 
        '''

        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)

        return doc1.similarity(doc2)

    def generate_recommendations(self, prompt, search_config):
        '''
        Generate the Recommendations based on a prompt and a search Config

        Parameters
        ----------
        prompt : str
            The search_prompt for the recommendations

        search_config : SearchConfig
            The SearchConfig object that contains the filters for the search_engine
        '''
        processed_text = self.process(prompt)

        self.recipes = []
        with psycopg2.connect(NLPModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                search_query = search_config.to_sql()
                print(search_query)
                curs.execute(search_query)
            
                for params in curs:
                    tags = params[-1].split()
                    recipe = Recipe(*params[:-1], tags=tags)
                    recipe.set_similarity(self.compare(processed_text, recipe.get_tags()))
                    self.recipes.append(recipe)

                curs.execute('DROP TABLE total_calories_lookup;')


        self.recipes = sorted(self.recipes, key=lambda x: x.get_similarity(), reverse=True)

        return self.serialize_recipes()

    @staticmethod
    def load_model():
        return joblib.load(os.path.join(os.path.dirname(__file__), 'models', 'nlpmodel.joblib'))

    def save_model(self):
        joblib.dump(self, os.path.join(os.path.dirname(__file__), 'models', 'nlpmodel.joblib'))

    def serialize_recipes(self):
        serialized_recipes = []
        for recipe in self.recipes:
            serialized_recipes.append(recipe.__dict__)
        return serialized_recipes

    @staticmethod
    def get_connection_string():
        dbname = config('DBNAME')
        user = config('USER')
        password = config('PASSWORD')
        host = config('HOST')
        return f'dbname={dbname} user={user} password={password} host={host}'