from abc import abstractmethod

import os

class SearchFilter:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def to_sql(self):
        pass


class TermFilter(SearchFilter):
    def __init__(self, term):
        super().__init__('Term Filter')
        self.term = term.lower()

    def to_sql(self):  
        return f"LOWER(tcl.name) LIKE '%{self.term}%' OR LOWER(tcl.tags) LIKE '%{self.term}%' OR LOWER(rr.comment) LIKE '%{self.term}%'"


class CalorieFilter(SearchFilter):
    def __init__(self, min_calories, max_calories):
        super().__init__('Calorie Filter')
        self.min_calories = min_calories
        self.max_calories = max_calories
    
    def to_sql(self):
        return f'Y.total_calories >= {self.min_calories} AND Y.total_calories <= {self.max_calories}'


class IngredientFilter(SearchFilter):
    def __init__(self, ingredient):
        super().__init__('Ingredient Filter')
        self.ingredient = ingredient.lower()

    def to_sql(self):
        return f"LOWER(Z.name) NOT LIKE '%{self.ingredient}%' AND LOWER(Y.tags) NOT LIKE '%{self.ingredient}%'"


class SearchConfig(SearchFilter):
    def __init__(self):
        super().__init__("Search Config v1")
        self.term_filters = []
        self.ingredient_filters = []
        self.calorie_filter = None

    def set_term_filter(self, full_term):
        terms = full_term.split()
        for term in terms:
            self.term_filters.append(TermFilter(term))

    def set_calorie_filter(self, min_calories, max_calories):
        self.calorie_filter = CalorieFilter(min_calories, max_calories)

    def set_ingredient_filter(self, ingredient):
        self.ingredient_filters.append(IngredientFilter(ingredient))

    @staticmethod
    def create_new(request_post):
        search_config = SearchConfig()
        
        # Create Search Filter
        search_config.set_term_filter(request_post['search_term'])


        if 'filter_enabled' in request_post:
            # Create Calorie filter
            search_config.set_calorie_filter(request_post['min_calories'], request_post['max_calories'])
            
            # Create Ingredient Filter
            for field_name, field_value in request_post.items():
                if field_name not in ['csrfmiddlewaretoken', 'search_term', 'min_calories', 'max_calories', 'filter_enabled']:
                    search_config.set_ingredient_filter(field_value)

        
        return search_config

    @staticmethod
    def apply_filter_to_script(script, search_filter):
        if search_filter:
            script = script.replace('[Filters]', '\t' + search_filter.to_sql() + '\n[Filters]')
            return script
        else:
            return script

    @staticmethod
    def clean_query(query):
        return query.replace('\n[Filters]', ';')


    def to_sql(self):
        with open(os.path.join(os.path.dirname(__file__), 'scripts', 'search_script_template.sql')) as template:
            search_query = template.read()
            
            # Apply Term filter
            for tfilter in self.term_filters:
                search_query = SearchConfig.apply_filter_to_script(search_query, tfilter)

            # Apply Calorie Filter
            search_query = SearchConfig.apply_filter_to_script(search_query, self.calorie_filter)

            # Apply Ingredient filters
            for ifilter in self.ingredient_filters:
                search_query = SearchConfig.apply_filter_to_script(search_query, ifilter)

            search_query = SearchConfig.clean_query(search_query)

        return search_query