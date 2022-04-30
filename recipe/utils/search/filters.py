from recipe.utils.base.sql import SqlFilter

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


