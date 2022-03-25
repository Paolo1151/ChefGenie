from chefgenie.settings import BASE_DIR

from .search_engine.nlpmodel import NLPModel

import os

model = NLPModel('recipe_recipe')

model.save_model()
