import discord
from discord.ext import commands
import sqlite3 as sql

APP_ID = 958935022788821063
GUILD_ID = 958953145030021150
OUTPUT_ID = 958961458765516840
BUGREPORT_URL = "https://github.com/mxze16/novabot-dev/issues/new/choose"

command_help = {
    "misc": {
        "settings": {
            "main": {
                "prefix": "Allows you to modify the prefix for the guild.\n\nPassing `default` or `reset` as an argument will set the prefix to `>`, or the original prefix.\n\n`Example of command usage:`\n\n```>setup prefix <new_prefix>```"
            }
        },
    },
    "moderation": {

    },
    "utilities": {
        "ping": "Returns the latency of the bot.\n\n`Example of command usage:`\n\n```>ping```",
        "members": "Returns a list of embeds full of members within the role provided.\n\nLet's assume the name of the desired role is 'testingrole' and the ID of the role is 1234567890. The following should work as intended.\n\nYou can supply a partial lookup, for example 'testi', and it should be able to return the role as normal most of the time, assuming the lookup is precise.\n\nYou can supply the role id, for example '1234567890', and it will convert the id into the role, assuming the id is correct.\n\nOr you can simply ping the role (not recommended for a number of reasons).\n\n`Example of command usage:`\n\n```>members testi\n>members 1234567890\n>members @testingrole```",
    }
}
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class NBRoleConverter(commands.RoleConverter):
    async def convert(self, ctx, argument) -> discord.Role:
        role = discord.utils.find(lambda r: argument.lower() in r.name.lower(), ctx.guild.roles)
        if role is None:
            return await super().convert(ctx, argument)
        else:
            return role

class NBDurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd']:
            return (int(amount), unit)

async def start_db():
    db = sql.connect("./data/novadata.sqlite")
    c = db.cursor()
    return db, c

async def close_db(db, c):
    c.close()
    db.close()
