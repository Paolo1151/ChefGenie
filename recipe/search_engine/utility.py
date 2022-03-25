from decouple import config

def get_connection_string():
    dbname = config('DBNAME')
    user = config('USER')
    password = config('PASSWORD')
    return f'dbname={dbname} user={user} password={password}'