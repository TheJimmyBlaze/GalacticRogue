class TransactionCommandInterface:
    async def call(self, message, state):
        pass

class Transaction:
    def __init__(self, function: TransactionCommandInterface, state):
        self.function = function
        self.state = state

class Transactor:
    def __init__(self):
        self.transactions = {}

    def clear_transaction(self, discord_id):
        del self.transactions[discord_id] 

    def add_transaction(self, discord_id, transaction):
        self.transactions[discord_id] = transaction

    def find_transaction(self, discord_id):
        if discord_id in self.transactions.keys():
            return self.transactions[discord_id]