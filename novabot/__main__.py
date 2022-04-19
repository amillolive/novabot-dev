import discord
from discord.ext import commands
from novabot import GUILD_ID, OUTPUT_ID
import asyncio

with open("./secrets/token") as f:
    token = f.read().strip()

bot = commands.Bot(
    command_prefix = ">",
    intents = discord.Intents.all(),
    case_insensitive = True,
)

CommandTree = bot.tree

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

@bot.event
async def on_ready():
    print(f'{bcolors.WARNING}READY: Bot has been marked active.')

async def startup():
    async with bot:
        await bot.start(token)

asyncio.run(startup())