from chefgenie.settings import BASE_DIR

from .search_engine.nlpmodel import NLPModel

import os

# To change once postgresql db is made
model = NLPModel(os.path.join(BASE_DIR, 'db.sqlite3'), 'recipe_recipe')

model.save_model()
