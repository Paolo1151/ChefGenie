from matplotlib import pyplot as plt
from decouple import config
from io import BytesIO

import pandas as pd

import psycopg2
import os



class AnalyticsModel:
    def __init__(self):
        print('Initialized Analytics Model...')

    @staticmethod
    def make_graph():
        with psycopg2.connect(AnalyticsModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                curs.execute(
'''
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

        plt.switch_backend('AGG')
        f = plt.figure()
        plt.plot(df['date'], df['calories'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(os.path.dirname(__file__), '..', '..',  'media', 'analytics', 'graphs', 'MealHistory.jpeg'))
        plt.close(f)

    @staticmethod
    def get_connection_string():
        dbname = config('DBNAME')
        user = config('USER')
        password = config('PASSWORD')
        return f'dbname={dbname} user={user} password={password}'