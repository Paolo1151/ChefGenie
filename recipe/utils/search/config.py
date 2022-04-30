from recipe.utils.base.model import BaseObject
from recipe.utils.base.sql import SqlFilter

import os

class TermFilter(SqlFilter):
    def __init__(self, term):
        super().__init__('Term Filter')
        self.term = term.lower()

    def to_sql(self):  
        return self.parse_filter(f"LOWER(tcl.name) LIKE '%{self.term}%' OR LOWER(tcl.tags) LIKE '%{self.term}%' OR LOWER(rr.comment) LIKE '%{self.term}%'")


class CalorieFilter(SqlFilter):
    def __init__(self, min_calories, max_calories):
        super().__init__('Calorie Filter')
        self.min_calories = min_calories
        self.max_calories = max_calories
    
    def to_sql(self):
        return self.parse_filter(f'Y.total_calories >= {self.min_calories} AND Y.total_calories <= {self.max_calories}')


class IngredientFilter(SqlFilter):
    def __init__(self, ingredient):
        super().__init__('Ingredient Filter')
        self.ingredient = ingredient.lower()

    def to_sql(self):
        return self.parse_filter(f"LOWER(Z.name) NOT LIKE '%{self.ingredient}%' AND LOWER(Y.tags) NOT LIKE '%{self.ingredient}%'")


class SearchConfig(BaseObject):
    def __init__(self, user):
        super().__init__("Search Config v1")
        self.user = user
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
    def create_new(request_post, user):
        search_config = SearchConfig(user)
        
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
        with open(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'search_script_template.sql')) as template:
            search_query = template.read()

            self.filters[-1].toggle_last()

            for sfilter in self.filters:
                search_query = SearchConfig.apply_filter_to_query(search_query, sfilter)

            search_query = SearchConfig.clean_query(search_query)

        return search_query