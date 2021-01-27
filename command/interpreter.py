import discord
from module.character.commands import handle_character
from command.transactor import Transactor
from command.transactor import Transaction

command_prefix = '.'

def clean(raw):
    no_prefix = raw.replace(command_prefix, '')
    command = no_prefix.split()
    return command

async def interpret(message, connection, transactor):
    transaction = transactor.find_transaction(message.author)
    if transaction is not None:
        await transaction.function.call(message, transaction.state)
    else:
        raw = message.content
        if raw.startswith(command_prefix):
            await handle_command(raw, message, connection, transactor)

async def handle_command(raw, message, connection, transactor):
    command = clean(raw)
    if command[0].lower() in ['character', 'char', 'ch']:
        await handle_character(command, message, connection, transactor)
