from recipe.utils.recipe.model import RecipeModel
from sklearn.feature_extraction.text import TfidfVectorizer

import os
import spacy
import pandas as np
import psycopg2

class RecommendationEngine(RecipeModel):
    def __init__(self):
        super().__init__('Recommendation Engine v1')

        try:
            self.nlp = spacy.load('en_core_web_md')
        except:
            spacy.cli.download('en_core_web_md')
            self.nlp = spacy.load('en_core_web_md')

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

    def generate_recommendations(self, n):
        '''
        Generate Top n Recommendations based on Tag Similarity of foods that person ate, clicked, or reviewed

        Parameters
        -----------
            n : int
                Number of Recipe Recommendations to Return

        Returns
        -----------
            recipes : list
                A List of N Recipies from most recommended to least recommended
        '''
        pass


