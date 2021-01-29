import sys
import discord
from command.interpreter import Interpreter
from data.connection import DbConnection
from command.transactor import Transactor
from data.seed.schema import Schema

discord_client = discord.Client()

db_path = "galactic_rogue.sqlite"
db_connection = None

transactor = None

command_prefix = "."
interpreter = None

@discord_client.event
async def on_ready():
    print("Logged in as {0.user}".format(discord_client))

    try:
        global db_connection
        db_connection = DbConnection(db_path)
        Schema(db_connection).create()

        global transactor
        transactor = Transactor()

        global interpreter
        interpreter = Interpreter(command_prefix, db_connection, transactor)

    except:
        print("An critical error occured during startup, Galactic Rogue could not start")
        sys.exit()

    print("The Rogue is Ready!\n")

@discord_client.event
async def on_message(message):
    try:
        await interpreter.interpret(message)

    except:
        print(f"A critiical error occured reading the message: {message.content}")
        sys.exit()

# Read the token and start the server
with open("token.txt", "r") as file:
    token = file.read().replace("\n", "")
    discord_client.run(token)