import sys
import discord
import sqlite3
from sqlite3 import Error
from data.database import create_connection 
from command.interpreter import interpret

client = discord.Client()
db_connection = None

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

    global db_connection
    db_connection = create_connection()

    if db_connection is None:
        print('An error occured during startup, Galactic Rogue did not start')
        sys.exit()

    print('Galactic Rogue is ready to go!')

@client.event
async def on_message(message):
    await interpret(message, db_connection)


client.run('ODAxMzc5MTU0MjM4NzY3MTM0.YAf0fw.0T8TmzDy3S66McaE0N7gaPTNDa8')