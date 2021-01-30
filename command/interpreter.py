from datetime import datetime
from datetime import timedelta
from module.character import CharacterModule

class Interpreter:
    def __init__(self, prefix, timeout, connection, transactor):
        self.prefix = prefix
        self.timeout = timeout

        self.transactor = transactor

        self.character_module = CharacterModule(connection, transactor)
        
        print("Interpreter initiialized")

    async def interpret(self, message):
        raw = message.content.strip()

        if raw.startswith(self.prefix):
            print(f"Interpreting command: {raw}")
            self.transactor.clear_transaction(message.author.id)
            await self.__handle_command(raw, message)
            return

        transaction = self.transactor.find_transaction(message.author.id)
        if transaction is not None:
            if transaction.timestamp + timedelta(seconds=self.timeout) < datetime.now():
                timeout_message = "> Your {} command has timed out.".format(transaction.description)
                self.transactor.clear_transaction(message.author.id)
                print(f"An expired transaction has been cleared")

                await message.channel.send(timeout_message)
                return
            
            print(f"Processing transaction response: {transaction.description}, {raw}")
            await transaction.function(message, transaction.state)
            return

    async def __handle_command(self, raw, message):
        command = self.__clean(raw)
        if command[0].lower() in ["character", "char", "ch"]:
            if await self.character_module.handle_command(command, message):
                return
            
    def __clean(self, raw):
        no_prefix = raw.replace(self.prefix, "")
        command = no_prefix.split()
        return command
