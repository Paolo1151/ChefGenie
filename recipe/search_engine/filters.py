from abc import abstractmethod

import os

class SearchFilter:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def to_sql(self):
        pass


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
        return f"LOWER(Z.name) NOT LIKE '%{self.ingredient}%' and LOWER(Y.tags) not like '%{self.ingredient}%'"


class SearchConfig(SearchFilter):
    def __init__(self):
        super().__init__("Search Config v1")
        self.ingredient_filters = []
        self.calorie_filter = None

    def set_calorie_filter(self, min_calories, max_calories):
        self.calorie_filter = CalorieFilter(min_calories, max_calories)

    def set_ingredient_filter(self, ingredient):
        self.ingredient_filters.append(IngredientFilter(ingredient))

    @staticmethod
    def create_new(request_post):
        search_config = SearchConfig()
        search_config.set_calorie_filter(request_post['min_calories'], request_post['max_calories'])
        for field_name, field_value in request_post.items():
            if field_name not in ['csrfmiddlewaretoken', 'search_term', 'min_calories', 'max_calories', 'filter_enabled']:
                search_config.set_ingredient_filter(field_value)
        return search_config


    def to_sql(self):
        with open(os.path.join(os.path.dirname(__file__), 'scripts', 'ingredient_filter_template.sql')) as query:
            temp_query = query.read()

            if self.ingredient_filters:
                temp_query = temp_query.replace("[ingredient_filters]", 'WHERE\n[ingredient_filters]')
                for ingredient_filter in self.ingredient_filters:
                    temp_query = temp_query.replace("[ingredient_filters]", f'    {ingredient_filter.to_sql()}\n[ingredient_filters]')

            table_creation_query = temp_query.replace('[ingredient_filters]\n', '')

        with open(os.path.join(os.path.dirname(__file__), 'scripts', 'calorie_filter_template.sql')) as query:
            temp_query = query.read()

            if self.calorie_filter:
                temp_query = temp_query.replace("[calorie_filter]", f'WHERE\n    {self.calorie_filter.to_sql()}[calorie_filter];')
            
            filtered_recipes_query = temp_query.replace('[calorie_filter]', '')

        return (table_creation_query, filtered_recipes_query)