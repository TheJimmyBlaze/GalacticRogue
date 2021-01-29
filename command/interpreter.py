from module.character import CharacterModule

class Interpreter:
    def __init__(self, prefix, connection, transactor):
        self.prefix = prefix
        self.transactor = transactor

        self.character_module = CharacterModule(connection, transactor)
        
        print('Interpreter initiialized')

    async def interpret(self, message):
        transaction = self.transactor.find_transaction(message.author)
        if transaction is not None:
            await transaction.function(message, transaction.state)
        else:
            raw = message.content
            if raw.startswith(self.prefix):
                await self.handle_command(raw, message)

    async def handle_command(self, raw, message):
        command = self.clean(raw)
        if command[0].lower() in ['character', 'char', 'ch']:
            await self.character_module.handle_command(command, message)
            
    def clean(self, raw):
        no_prefix = raw.replace(self.prefix, '')
        command = no_prefix.split()
        return command
