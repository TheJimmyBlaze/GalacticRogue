import sqlite3
from data.connection import DbConnection

async def create_character(message, connection):
    races = connection.get_query("SELECT display_name, description FROM race")
    
    race_list = ""
    for race in races:
        race_list += "```{}: {}```".format(race[0], race[1])
    
    prompt = "> Which race are you?\n{}".format(race_list)

    await message.channel.send(prompt)


async def handle_character(command, message, connection):
    if command[1].lower() == 'create':
        await create_character(message, connection)