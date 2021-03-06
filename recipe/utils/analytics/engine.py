from decouple import config
from io import BytesIO
from recipe.utils.base.model import BaseModel

import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import datetime as dt

import psycopg2
import os
import base64
import datetime

class AnalyticsEngine(BaseModel):
    def __init__(self):
        super().__init__('Analytics Model v1')

    @staticmethod
    def generate_last_n_days(n):
        today = datetime.datetime.today()
        date_df = pd.date_range(
            end=f'{today.month}/{today.day}/{today.year}',
            periods=n,
            freq='D'
        )
        return pd.DataFrame(date_df, columns=['date'])

    @staticmethod
    def graph_calorie_intake(user_id, days_offset, goal):
        with psycopg2.connect(BaseModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                with open(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'calorie_intake_all.sql')) as query:
                    intake_query = query.read()
                    intake_query = intake_query.replace('[USERID]', str(user_id))
                    curs.execute(intake_query)

                    meal_history = {'date': [], 'calories': []}
                    for entry in curs:
                        meal_history['date'].append(entry[0])
                        meal_history['calories'].append(entry[1])

                    df = pd.DataFrame(meal_history)
                    df['date'] = pd.to_datetime(df['date'])

                    date_df = AnalyticsEngine.generate_last_n_days(days_offset)
                    
                    merged_df = date_df.merge(df, left_on='date', right_on='date', how='left')
                    merged_df = merged_df.fillna(0).sort_values(by='date', ascending=False)
                    
        return AnalyticsEngine._generate_graph(merged_df, goal)

    @staticmethod
    def table_calorie_intake(user_id, days_offset):
        with psycopg2.connect(BaseModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                with open(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'calorie_intake_all.sql')) as query:
                    intake_query = query.read()
                    intake_query = intake_query.replace('[USERID]', str(user_id))
                    curs.execute(intake_query)

                    meal_history = {'date': [], 'calories': [], }
                    for entry in curs:
                        meal_history['date'].append(entry[0])
                        meal_history['calories'].append(entry[1])

                    df = pd.DataFrame(meal_history, columns=['date', 'calories'])
                    df['date'] = pd.to_datetime(df['date'])

                    date_df = AnalyticsEngine.generate_last_n_days(days_offset)
                    
                    merged_df = date_df.merge(df, left_on='date', right_on='date', how='left')
                    merged_df = merged_df.fillna(0).sort_values(by='date', ascending=True)
                    
        return AnalyticsEngine._generate_table(merged_df) 

    @staticmethod
    def pie_chart_ingredients(user_id, days_offset):
        with psycopg2.connect(BaseModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                with open(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'ingredients_chart.sql')) as query:
                    intake_query = query.read()
                    intake_query = intake_query.replace('[USERID]', str(user_id))
                    curs.execute(intake_query)

                    ingredient_history = {'category': [], 'count': [],}
                    for entry in curs:
                        if entry[0] == 'condiment' or entry[0] == 'spices' or entry[0] == 'miscellaneous' or entry[0] == 'herb':
                            continue
                        else: 
                            ingredient_history['category'].append(entry[0])
                            ingredient_history['count'].append(entry[1])

                    df = pd.DataFrame(ingredient_history)
        return AnalyticsEngine._generate_chart(df)

    @staticmethod
    def table_recent_meals(user_id):
        with psycopg2.connect(BaseModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                with open(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'five_recent_meals.sql')) as query:
                    intake_query = query.read()
                    intake_query = intake_query.replace('[USERID]', str(user_id))
                    curs.execute(intake_query)

                    meal_history = {'date': [], 'name':[], 'calories': [], }
                    for entry in curs:
                        meal_history['date'].append(entry[0])
                        meal_history['name'].append(entry[1])
                        meal_history['calories'].append(entry[2])
                    
                    if len(meal_history['date']) < 5:
                        difference = 5 - len(meal_history['date']) 
                        for a in range(0,difference):
                            meal_history['date'].append('-')
                            meal_history['name'].append('-')
                            meal_history['calories'].append('-')

                    df = pd.DataFrame(meal_history, columns=['date', 'name', 'calories'])
                    print(len(meal_history['date']))

        return AnalyticsEngine._generate_table(df) 

    @staticmethod
    def _generate_graph(df, goal):
        fig = plt.figure()

        plt.plot(df['date'], df['calories'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        max_cal = max(df['calories'])

        plt.ylim(-0.05*max_cal, max_cal*1.05)

        plt.axhline(y = goal, color = 'r', linestyle = '-')
        
        plt.text(df['date'][2], goal, "Calorie Goal")

        plt.xlabel("Date")
        plt.ylabel("Calories")

        flike = BytesIO()
        fig.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()

        plt.close(fig)

        return {'graph': b64}


    @staticmethod
    def _generate_chart(df):
        fig = plt.figure()
        plt.pie(df['count'],labels=df['category'], autopct='%1.1f%%')
        plt.axis('equal')
        plt.tight_layout()

        flike = BytesIO()
        fig.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()

        plt.close(fig)

        return b64

    @staticmethod
    def _generate_table(df):
        table = df
        fixed_table = table.to_html(index=False, justify='center')
        return fixed_table