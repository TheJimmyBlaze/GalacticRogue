import sqlite3
from data.connection import DbConnection
from module.character.character_creator import create_character

async def handle_character(command, message, connection, transactor):
    if command[1].lower() == 'create':
        await create_character(message, connection, transactor)