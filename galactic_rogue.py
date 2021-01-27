import sys
import discord
import sqlite3
from sqlite3 import Error
from data.database import create_connection 
from command.interpreter import interpret
from command.transactor import Transactor

client = discord.Client()
db_connection = None

transactor = Transactor()

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
    await interpret(message, db_connection, transactor)

with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')
    client.run(token)