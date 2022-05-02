from decouple import config
from io import BytesIO
from recipe.utils.base.model import BaseModel

import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

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
    def graph_calorie_intake(user_id, days_offset):
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
                    
        return AnalyticsEngine._generate_graph(merged_df)

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
    def _generate_graph(df):
        fig = plt.figure()

        plt.plot(df['date'], df['calories'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        max_cal = max(df['calories'])

        plt.ylim(-0.05*max_cal, max_cal*1.05)

        flike = BytesIO()
        fig.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()

        plt.close(fig)

        return {'graph': b64}

    @staticmethod
    def _generate_table(df):
        table = df
        fixed_table = table.to_html(index=False, justify='center')
        return fixed_table