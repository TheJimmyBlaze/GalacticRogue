import discord
from module.character.commands import handle_character

command_prefix = '.'

def clean(raw):
    no_prefix = raw.replace(command_prefix, '')
    command = no_prefix.split()
    return command

async def handle_command(raw, message, connection):
    command = clean(raw)
    if command[0].lower() in ['character', 'char', 'ch']:
        await handle_character(command, message, connection)

async def interpret(message, connection):
    raw = message.content
    if raw.startswith(command_prefix):
        await handle_command(raw, message, connection)
