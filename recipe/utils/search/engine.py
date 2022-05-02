from recipe.utils.recipe.model import RecipeModel

import pandas as pd
import numpy as np
import spacy
import psycopg2
import os

class SearchEngine(RecipeModel):
    def __init__(self):
        '''Create an NLP Processor with an internal nlp object for nlp operations'''
        super().__init__('Search Model v1')
        self.calorie_recommendations = []

    def generate_search_results(self, prompt, search_config):
        '''
        Generate the Recommendations based on a prompt and a search Config

        Parameters
        ----------
        prompt : str
            The search_prompt for the recommendations

        search_config : SearchConfig
            The SearchConfig object that contains the filters for the search_engine

        Returns
        ----------
        recipes : dict
            A Dictionary of Two Dictionaries that contains Recipe Objects that are serialized.
            Goal_Recipes: Recipes that fit the goal
            Other Recipes: Recipes that fit the term, but goes above the goal
        '''
        calorie_goal = self.calculate_calorie_goal(search_config.user)
        
        self.flush_pool()

        self.fill_results(search_config)

        self.partition_results(calorie_goal)

        return dict(
            goal_recipes=SearchEngine.package_recipes(self.goal_recipes),
            other_recipes=SearchEngine.package_recipes(self.recipes)
        ) 

    @staticmethod
    def calculate_calorie_goal(user):
        with psycopg2.connect(SearchEngine.get_connection_string()) as conn:
            with conn.cursor() as curs:
                with open(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'calorie_intake_today.sql')) as query:
                    intake_query = query.read()
                    intake_query = intake_query.replace('[USERID]', str(user.user_id))
                    curs.execute(intake_query)

                    query_result = curs.fetchone()

                    current_calories = 0 if not query_result else query_result[1]
        return user.calorie_goal - current_calories

    def fill_results(self, search_config):
        with psycopg2.connect(SearchEngine.get_connection_string()) as conn:
            with conn.cursor() as curs:
                search_query = search_config.generate_query()
                curs.execute(search_query)
            
                for params in curs:
                    self.add_new_recipe(params)

                curs.execute('DROP TABLE total_calories_lookup;')

    def partition_results(self, calorie_goal):
        self.goal_recipes = list(filter(lambda x: x.calories <= calorie_goal, self.recipes))
        self.recipes = list(filter(lambda x: x.calories > calorie_goal, self.recipes))



