

class Recipe:
    def __init__(self, name, tags):
        '''
        Parameters
        ----------
        name : str
            Name of the Recipe

        tags : list (str)
            String Tags associated with the object
        '''
        self.name = name
        self.tags = tags