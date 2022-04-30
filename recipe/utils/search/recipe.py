class Recipe:
    def __init__(self, id, name, tags, *args, **kwargs):
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
        self.id = id
        self.name = name
        self.tags = tags.split()
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