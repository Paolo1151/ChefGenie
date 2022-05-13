from recipe.utils.base.model import BaseObject
from recipe.utils.base.model import BaseModel


class Recipe(BaseObject):
    def __init__(self, id, name, tags, calories=0, *args, **kwargs):
        '''
        Parameters
        ----------
        id: int
            ID of the Recipe

        name : str
            Name of the Recipe

        tags : set (str)
            String Tags associated with the object
        '''
        super().__init__(name)

        self.id = id
        self.tags = tags.split()
        self.calories = calories

        self.similarity = 0
    
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_similarity(self):
        return self.similarity

    def set_similarity(self, value):
        self.similarity = value

    def get_tags(self):
        return " ".join(self.tags)

    def add_tag(self, value):
        self.tags.add(val)

    def add_range_tags(self, value):
        for val in value:
            self.tags.add(val)

    def remove_tag(self, value):
        del self.tags[value]

    def __str__(self):
        return f"{name}: {tags}"


class RecipeModel(BaseModel):
    def __init__(self, name):
        super().__init__(name)
        self.recipes = []

    def add_new_recipe(self, params):
        self.recipes.append(Recipe(*params))

    def flush_pool(self):
        self.recipes = []

    def fill_pool(self):
        with psycopg2.connect(RecipeModel.get_connection_string()) as conn:
            with conn.cursor() as curs:
                curs.execute('SELECT * FROM recipe_recipe')

                for row in curs:
                    self.add_new_recipe(row[-1])
    @staticmethod
    def package_recipes(recipe_list):
        serialized_recipes = []
        for recipe in recipe_list:
            serialized_recipes.append(recipe.__dict__)
        return serialized_recipes