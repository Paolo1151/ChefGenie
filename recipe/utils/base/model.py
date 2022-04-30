from decouple import config

class BaseObject:
    def __init__(self, name):
        self.name = name

class BaseModel(BaseObject):
    def __init__(self, name):
        super().__init__(name)
        print(f'Initialized {name}...')

    @staticmethod
    def get_connection_string():
        dbname = config('DBNAME')
        user = config('USER')
        password = config('PASSWORD')
        host = config('HOST')
        return f'dbname={dbname} user={user} password={password} host={host}'