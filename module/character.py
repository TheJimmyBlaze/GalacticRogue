import re
from command.transactor import Transaction
from command.transactor import DefaultState

create_character_transaction = "Create Character"

class CharacterModule:
    def __init__(self, connection, transactor):
        self.connection = connection
        self.transactor = transactor

    async def handle_command(self, command, message):
        if (command[0].lower() in ["character", "char", "ch"]):
            if command[1].lower() == "create":
                await self.__create_character(message) 
                return True
        return False

    async def __create_character(self, message):
        existing_character = self.connection.get_query("SELECT display_name FROM character WHERE discord_id = ?", [message.author.id])[0][0]
        if existing_character:
            await message.channel.send("> You've been here before. I remember you as {}.".format(existing_character))
            return

        await self.__prompt_race(message)

    async def __prompt_race(self, message):
        races = self.connection.get_query("SELECT display_name, description FROM race")
        
        race_list = ""
        for race in races:
            race_list += "```{}: {}```".format(race[0], race[1])
        
        prompt = "> Ahh a new traveller, tell me about yourself.\n> Which race do you belong to?\n{}".format(race_list)

        transaction = Transaction(create_character_transaction, self.__prompt_background, DefaultState())
        self.transactor.add_transaction(message.author.id, transaction)

        await message.channel.send(prompt)

    async def __prompt_background(self, message, state):
        chosen_race = message.content.strip()
        races = self.connection.get_query("SELECT natural_id, display_name, observation FROM race")

        for race in races:
            if race[1].lower() == chosen_race:
                backgrounds = self.connection.get_query("SELECT display_name, description FROM background")

                background_list = ""
                for background in backgrounds:
                    background_list += "```{}: {}```".format(background[0], background[1])

                prompt = "> A {} then, {}\n> Tell me about your background.\n{}".format(race[1], race[2], background_list)

                state.race_id = race[0]
                state.race_name = race[1]
                transaction = Transaction(create_character_transaction, self.__prompt_name, state)
                self.transactor.add_transaction(message.author.id, transaction)

                await message.channel.send(prompt)
                return

    async def __prompt_name(self, message, state):
        chosen_background = message.content.strip()
        backgrounds = self.connection.get_query("SELECT natural_id, display_name, observation FROM background")

        for background in backgrounds:
            if background[1].lower() == chosen_background:
                prompt = "> I could tell you were a {}, {}\n> And what is your name?".format(background[1], background[2])

                state.background_id = background[0]
                state.background_name = background[1]
                transaction = Transaction(create_character_transaction, self.__commit_character_create, state)
                self.transactor.add_transaction(message.author.id, transaction)

                await message.channel.send(prompt)
                return

    async def __commit_character_create(self, message, state):
        name = message.content.strip()

        name_regex = "^[A-z'-]{2,25}( [A-z'-]{2,25})?$"
        pattern = re.compile(name_regex)

        if pattern.match(name):

            query = """
            INSERT INTO character (
                race_id,
                background_id,
                discord_id,
                display_name
            ) VALUES ( 
                ?,
                ?,
                ?,
                ?
            );
            """
            self.connection.execute_query(query, [state.race_id, state.background_id, message.author.id, name])

            prompt = "> Welcome {}, it's not every day you see a {} {}".format(name, state.race_name, state.background_name)
            await message.channel.send(prompt)

            self.transactor.clear_transaction(message.author.id)
            return
        
        await message.channel.send("> The name {} is too complex, it may only contain letters apostrophes hyphens and a single space.")
        
