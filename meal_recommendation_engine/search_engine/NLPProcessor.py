from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
import numpy as np

import spacy


class NLPProcessor:
    def __init__(self):
        '''Create an NLP Processor with an internal nlp object for nlp operations'''
        self.nlp = spacy.load('en_core_web_lg')

    def recommend(self, prompt, pool):
        '''
        Attributes:
        -----------
        prompt : str
            The prompt used to determine recommendations.
        pool : Dict<str, str>
            The recommendation pool with names as the keys and the tags as the values.

        Returns:
        -----------
        sorted_recommendations : List
            Ordered list of recommendations based on score
        '''
        processed_text = self.process(prompt)

        scores = {}
        for name, tags in pool.items():
            scores[name] = self.compare(processed_text, tags)
        
        score_list = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return score_list

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