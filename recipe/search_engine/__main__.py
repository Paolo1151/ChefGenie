import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ''))

from .nlpmodel import NLPModel

nlpp = NLPModel(os.path.join(os.path.dirname(__file__), 'test', 'test.sqlite3'), 'recipe')

def main():
    parser = argparse.ArgumentParser(description = 'NLP Model CLI')
    parser.add_argument('--function', help='function', type=str)
    parser.add_argument('--text', help='text', type=str)
    parser.add_argument('--text1', help='text1', type=str)
    parser.add_argument('--text2', help='text2', type=str)

    test_objects = {
        "Pepperoni Pizza": "Pizza Egg Bake Dough Oil Tomato Salty Pepperoni Cheese Snack Lunch Fancy Party",
        "Omelette": "Egg Salty Breakfast Omelette",
        "Bacon": "Pork Fried Oil Fats Breakfast Salty Bacon",
        "Ceasar Salad": "Vegetables Greens Healthy Lettuce Savory Carrots Salad",
        "Beef Tapa": "Beef Fats Oils Savory Salty Filipino Tapa Breakfast",
        "Pancake": "Breakfast Sweet Pastry Egg Pancake",
        "Steak": "Beef Steak Fancy Date Savory Dinner",
        "Mushroom Soup": "Soup Mushroom Savory Lunch Breakfast Dinner",
        "Fried Rice": "Rice Fried Shrimp Butter Savory Lunch Breakfast Dinner",
        "Spaghetti": "Noodles Spaghetti Savory Cheese Tomato Snack Lunch Breakfast Dinner",
    }

    args = parser.parse_args()

    function = args.function
    text = args.text
    text1 = args.text1
    text2 = args.text2

    if function == 'process':
        print(f'Input: {text}')
        result = nlpp.process(text)
        print(f'Result: {result}')
    elif function == 'compare':
        print(f'Inputs: {text1}, {text2}')
        result = nlpp.compare(text1, text2)
        print(f'Result: {result}')
    elif function == 'recommend':
        print(f'Input: {text}')
        result = nlpp.generate_recommendations(text)
        print('Result: ')
        for i, recipe in enumerate(result):
            name = recipe['name']
            score = recipe['similarity']
            print(f'{i+1}. {name} : {score}')
    elif function == 'save':
        nlpp.save_model()
        print('Successfully Saved Model!')
    elif function == 'load':
        test_model = NLPModel.load_model()
        print('Successfully Loaded Model!')



if __name__ == '__main__':
    main()