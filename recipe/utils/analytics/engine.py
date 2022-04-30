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
    def analyze_calorie_intake(user_id):
        with psycopg2.connect(BaseModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                with open(os.path.join(os.path.dirname(__file__), 'scripts', 'calorie_intake.sql')) as query:
                    intake_query = query.read()
                    intake_query = intake_query.replace('[USERID]', str(user_id))
                    curs.execute(intake_query)

                    meal_history = {'date': [], 'calories': []}
                    for entry in curs:
                        meal_history['date'].append(entry[0])
                        meal_history['calories'].append(entry[1])

                    df = pd.DataFrame(meal_history)
                    df['date'] = pd.to_datetime(df['date'])

                    today = datetime.datetime.today()
                    date_df = pd.DataFrame([today - datetime.timedelta(days=offset) for offset in range(0, 7)], columns=['date'])

                    merged_df = date_df.join(df, on='date', lsuffix='_x', rsuffix='_y', sort=True)

                    merged_df.drop(columns=['date_x', 'date_y'], inplace=True)
                    merged_df = merged_df.fillna(0)

                    print(merged_df)

        return AnalyticsEngine._generate_graph(merged_df)

    @staticmethod
    def _generate_graph(df):
        fig = plt.figure()

        plt.plot(df['date'], df['calories'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        max_cal = max(df['calories']) + 10

        plt.ylim(-1, max_cal)

        flike = BytesIO()
        fig.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()

        plt.close(fig)

        return {'graph': b64}