from command.transactor import Transaction

class CharacterModule:
    def __init__(self, connection, transactor):
        self.connection = connection
        self.transactor = transactor

    async def handle_command(self, command, message):
        if (command[0].lower() in ['character', 'char']):
            if command[1].lower() == 'create':
                await self.create_new(message)

    async def create_new(self, message):
        await self.__prompt_race(message)

    async def __prompt_race(self, message):
        races = self.connection.get_query("SELECT display_name, description FROM race")
        
        race_list = ""
        for race in races:
            race_list += "```{}: {}```".format(race[0], race[1])
        
        prompt = "> Which race are you?\n{}".format(race_list)

        transaction = Transaction(self.__confirm_race, None)
        self.transactor.add_transaction(message.author, transaction)

        await message.channel.send(prompt)

    async def __confirm_race(self, message, state):
        chosen_race = message.content
        races = self.connection.get_query("SELECT natural_id, display_name FROM race")

        for race in races:
            if race[1].lower() == chosen_race:
                print(f'Selected Race: {race[0]}')
                self.transactor.clear_transaction(message.author)
                return