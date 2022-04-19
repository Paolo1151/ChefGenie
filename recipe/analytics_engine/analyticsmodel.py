from matplotlib import pyplot as plt 
from decouple import config


import pandas as pd

import spacy
import psycopg2
import os



class AnalyticsModel:
    def __init__(self):
        pass

    @staticmethod
    def make_graph():
        with psycopg2.connect(AnalyticsModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                curs.execute('SELECT id, calories FROM recipe_mealmade')

                meal_history = {'id': [], 'calories': []}
                for entry in curs:
                    meal_history['id'].append(entry[0])
                    meal_history['calories'].append(entry[1])
        df = pd.DataFrame(meal_history)
        plt.figure()
        plt.plot(df['id'], df['calories]'])
        plt.savefig(os.phat.join(os.path.dirname(__file__), '..', 'media', 'fig', 'MealHistory.Jpg'))

    @staticmethod
    def get_connection_string():
        dbname = config('DBNAME')
        user = config('USER')
        password = config('PASSWORD')
        return f'dbname={dbname} user={user} password={password}'