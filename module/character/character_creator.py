from command.transactor import Transaction

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

    state = RaceTransactionState(connection, transactor)
    transaction = Transaction(RaceTransactionCommand(), state)
    transactor.add_transaction(message.author, transaction)

    await message.channel.send(prompt)

class RaceTransactionState:
    def __init__(self, connection, transactor):
        self.connection = connection
        self.transactor = transactor

class RaceTransactionCommand:
    async def call(self, message, state):
        chosen_race = message.content
        races = state.connection.get_query("SELECT natural_id, display_name FROM race")

        for race in races:
            if race[1].lower() == chosen_race:
                commit_character(message, race[0], state.transactor) 
                return