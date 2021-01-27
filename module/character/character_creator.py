import discord
from command.transactor import TransactionCommandInterface
from command.transactor import Transaction
from command.transactor import Transactor

async def create_character(message, connection, transactor):
    await prompt_race(message, connection, transactor)

def commit_character(message, race_id, transactor):
    print('selected race: {}'.format(race_id))
    transactor.clear_transaction(message.author)

async def prompt_race(message, connection, transactor):
    races = connection.get_query("SELECT display_name, description FROM race")
    
    race_list = ""
    for race in races:
        race_list += "```{}: {}```".format(race[0], race[1])
    
    prompt = "> Which race are you?\n{}".format(race_list)

    state = RaceTransactionState(connection)
    transaction = Transaction(RaceTransactionCommand(), state)
    transactor.add_transaction(message.author, transaction)

    await message.channel.send(prompt)

class RaceTransactionState:
    
    def __init__(self, connection):
        self.connection = connection

class RaceTransactionCommand(TransactionCommandInterface):

    def select_race(self, message, chosen_race, races, transactor):
        for race in races:
            if race[1].lower() == chosen_race:
                commit_character(message, race[0], transactor) 
                return

    async def call(self, message, state, transactor):
        chosen_race = message.content
        races = state.connection.get_query("SELECT natural_id, display_name FROM race")
        self.select_race(message, chosen_race, races, transactor)