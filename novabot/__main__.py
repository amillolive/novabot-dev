import discord
from discord.ext import commands
from novabot import APP_ID, GUILD_ID, OUTPUT_ID, bcolors
import asyncio
import os

with open("./secrets/token") as f:
    token = f.read().strip()

bot = commands.Bot(
    application_id = APP_ID,
    command_prefix = ">",
    intents = discord.Intents.all(),
    case_insensitive = True,
)

bot.default_colour = discord.Colour.from_rgb(r=0, g=0, b=255)

for filename in os.listdir('./novabot/cogs'):
    if filename.endswith('.py'):
        cog = filename[:-3]
        bot.load_extension(f'novabot.cogs.{cog}')
        print(f'{bcolors.WARNING}LOG: "{cog}" cog has been loaded.')

bot.run(token)