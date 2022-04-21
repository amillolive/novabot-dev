import discord
from discord.ext import commands

APP_ID = 958935022788821063
GUILD_ID = 958953145030021150
OUTPUT_ID = 958961458765516840
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
    async def convert(self, ctx, argument):
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