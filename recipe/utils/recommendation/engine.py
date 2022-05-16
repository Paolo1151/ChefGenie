from recipe.utils.recipe.model import RecipeModel
from sklearn.feature_extraction.text import TfidfVectorizer

import os
import spacy
import pandas as np
import psycopg2
import random

class RecommendationEngine(RecipeModel):
    def __init__(self):
        super().__init__('Recommendation Engine v1')

        try:
            self.nlp = spacy.load('en_core_web_md')
        except:
            spacy.cli.download('en_core_web_md')
            self.nlp = spacy.load('en_core_web_md')

        self.new_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'recom_script_new.sql')
        self.cat_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'recom_script_cat.sql')
        self.rev_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'recom_script_rev.sql')

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

    def compare_top3(self, top3tags, comptags):
        '''
        Attributes:
        -----------
        top3tags : list
            List of recipe tags from the top 3 recipes of the user

        comptags : str
            Recipe tags to compare with top 5

        Returns:
        -----------
        similarity : float
            The document similarity score of the two texts 
        '''
        avg_sim = 0

        for best in top3tags:
            avg_sim += self.compare(best, comptags)
        
        avg_sim /= 3

        return avg_sim

    def generate_recommendations(self, n, recommendation_type, user_id):
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
        recommendations = []

        if recommendation_type == 'new':
            with psycopg2.connect(RecommendationEngine.get_connection_string()) as conn:
                with conn.cursor() as curs:
                    with open(self.new_path) as q:
                        template = q.read()
                        template = template.replace('[USERID]', str(user_id))

                        curs.execute(template)

                        for row in curs:
                            recommendations.append((row[0], row[1]))

                        if len(recommendations) > n:
                            recommendations = random.sample(recommendations, k=n)

        elif recommendation_type == 'category':
            with psycopg2.connect(RecommendationEngine.get_connection_string()) as conn:
                with conn.cursor() as curs:
                    with open(self.cat_path) as q:
                        template = q.read()
                        template = template.replace('[USERID]', str(user_id))
                        curs.execute(template)
                        for row in curs:
                            recommendations.append((row[0], row[1]))

                        if len(recommendations) > n:
                            recommendations = random.sample(recommendations, k=n)
                        

        elif recommendation_type == 'review':
            with psycopg2.connect(RecommendationEngine.get_connection_string()) as conn:
                with conn.cursor() as curs:
                    with open(self.rev_path) as q:
                        template = q.read()
                        template = template.replace('[USERID]', str(user_id))
                        curs.execute(template)
                        top3 = []
                        top3_id = []
                        for row in curs:
                            top3_id.append(row[0])
                            top3.append(row[1])

                        if len(top3) > 0:
                            self.fill_pool()

                        for recipe in self.recipes:
                            if recipe.id in top3_id:
                                recipe.set_similarity(0)
                            else:
                                recipe.set_similarity(self.compare_top3(top3, recipe.get_tags()))

                        recommendations_recp = sorted(self.recipes, key=lambda x: x.get_similarity(), reverse=True)[:n]

                        recommendations = [(recipe.id, recipe.get_name()) for recipe in recommendations_recp]

        return recommendations


