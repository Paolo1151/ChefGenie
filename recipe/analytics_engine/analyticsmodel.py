import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from decouple import config
from io import BytesIO


import pandas as pd

import psycopg2
import os
import base64

##############################################
# URGENT: Investigate why Matplotlib backend change wont work
##############################################

class AnalyticsModel:
    def __init__(self):
        print('Initialized Analytics Model...')

    @staticmethod
    def make_graph(user_id):
        with psycopg2.connect(AnalyticsModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    f'''
                    SELECT
                        m.date,
                        SUM(m.total_calories) as calories_per_day
                    FROM
                    (
                        SELECT 
                            x.id,
                            x.date,
                            x.recipe_id,
                            x.user_id,
                            SUM(A.calories * Z.required_amount * X.amount) AS total_calories
                        FROM 
                            recipe_mealmade X
                            inner join recipe_recipe Y on X.recipe_id = Y.id
                            inner join recipe_requirement Z on Z.recipe_id = Y.id
                            inner join recipe_ingredient A on A.id = Z.id
                        GROUP BY
                            x.id,
                            x.date,
                            x.recipe_id,
                            x.user_id
                    ) m
                    WHERE
                        m.user_id = {user_id}
                    GROUP BY
                        m.date 
                    ORDER BY
                        m.date
                    FETCH FIRST 7 ROWS ONLY
                    '''
                )

                meal_history = {'date': [], 'calories': []}
                for entry in curs:
                    meal_history['date'].append(entry[0])
                    meal_history['calories'].append(entry[1])

        df = pd.DataFrame(meal_history)
        df['date'] = pd.to_datetime(df['date'])


        fig = plt.figure()
        
        plt.plot(df['date'], df['calories'])
        plt.xticks(rotation=45)
        plt.tight_layout()

        flike = BytesIO()
        fig.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()


        return {'graph': b64}

    @staticmethod
    def get_connection_string():
        dbname = config('DBNAME')
        user = config('USER')
        password = config('PASSWORD')
        return f'dbname={dbname} user={user} password={password}'