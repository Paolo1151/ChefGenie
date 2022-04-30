from recipe.utils.base.model import BaseObject

from .filters import TermFilter
from .filters import CalorieFilter
from .filters import IngredientFilter

import os

class SearchConfig(BaseObject):
    def __init__(self):
        super().__init__("Search Config v1")
        self.filters = []

    def append_term_filter(self, full_term):
        terms = full_term.split()
        for term in terms:
            self.filters.append(TermFilter(term))

    def append_calorie_filter(self, min_calories, max_calories):
        self.filters.append(CalorieFilter(min_calories, max_calories))

    def append_ingredient_filter(self, ingredient):
        self.filters.append(IngredientFilter(ingredient))

    @staticmethod
    def create_new(request_post):
        search_config = SearchConfig()
        
        # Create Search Filter
        search_config.append_term_filter(request_post['search_term'])

        if 'filter_enabled' in request_post:
            # Create Calorie filter
            search_config.append_calorie_filter(request_post['min_calories'], request_post['max_calories'])
            
            # Create Ingredient Filter
            for field_name, field_value in request_post.items():
                if field_name not in ['csrfmiddlewaretoken', 'search_term', 'min_calories', 'max_calories', 'filter_enabled']:
                    search_config.append_ingredient_filter(field_value)

        
        return search_config

    @staticmethod
    def apply_filter_to_query(script, search_filter):
        if search_filter:
            script = script.replace('[Filters]', '\t' + search_filter.to_sql() + '\n[Filters]')
            return script
        else:
            return script

    @staticmethod
    def clean_query(query):
        return query.replace('\n[Filters]', ';')

    def generate_query(self):
        with open(os.path.join(os.path.dirname(__file__), 'scripts', 'search_script_template.sql')) as template:
            search_query = template.read()

            self.filters[-1].toggle_last()

            for sfilter in self.filters:
                search_query = SearchConfig.apply_filter_to_query(search_query, sfilter)

            search_query = SearchConfig.clean_query(search_query)

        return search_query