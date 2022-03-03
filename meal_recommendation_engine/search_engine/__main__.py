import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ''))

from .NLPProcessor import NLPProcessor

nlpprocessor = NLPProcessor()

def main():
    parser = argparse.ArgumentParser(description = 'NLP Processor CLI')
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
        result = nlpprocessor.process(text)
        print(f'Result: {result}')
    elif function == 'compare':
        print(f'Inputs: {text1}, {text2}')
        result = nlpprocessor.compare(text1, text2)
        print(f'Result: {result}')
    elif function == 'recommend':
        print(f'Input: {text}')
        result = nlpprocessor.recommend(text, test_objects)
        print('Result: ')
        for i, (name, score) in enumerate(result):
            print(f'{i+1}. {name} : {score}')


if __name__ == '__main__':
    main()