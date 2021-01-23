import sqlite3
from sqlite3 import Error
from data.connection import DbConnection
from data.seed.schema import setup

sql_path = 'galactic_rogue.sqlite'

def create_connection():
    path = sql_path
    connection = None
    try:
        print(f'Connecting to DB: {path}...')
        connection = sqlite3.connect(path)
        print(f'Connection to DB: {path} established')

        db = DbConnection(connection)

        print(f'Ensuring DB updated...')
        setup(db)
        print(f'DB up to date')
        
    except Error as e:
        print(f'Error: {e}')
        return None

    return db