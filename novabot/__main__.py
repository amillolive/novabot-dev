import discord
from discord import slash_command
from discord.ext import commands
from typing import Optional
from novabot import bcolors, GUILD_ID, NBRoleConverter, APP_ID, start_db, close_db
from datetime import datetime
import asyncio
import os
import sqlite3 as sql

with open("./secrets/token") as f:
    token = f.read().strip()

async def get_prefix(bot, message):
    if not message.guild:
        return ">"
    
    db, c = await start_db()

    c.execute(f"SELECT * FROM main WHERE guild_id = {message.guild.id}")
    result = c.fetchone()

    if result is None:
        sqldata = ("INSERT INTO main(guild_id, mod_id, log_id, prefix, owner_id) VALUES(?, ?, ?, ?, ?)")
        vals = (message.guild.id, None, None, ">", message.guild.owner_id)
        c.execute(sqldata, vals)
        db.commit()
    
    c.execute(f"SELECT prefix FROM main WHERE guild_id = {message.guild.id}")
    result = c.fetchone()

    await close_db(db, c)
    return result[0]

bot = commands.Bot(
    application_id = APP_ID,
    command_prefix = get_prefix,
    intents = discord.Intents.all(),
    case_insensitive = True,
)

bot.default_colour = discord.Colour.from_rgb(r=0, g=0, b=255)
bot.default_error = discord.Colour.from_rgb(r=255, g=0, b=0)

for filename in os.listdir('./novabot/cogs'):
    if filename.endswith('.py'):
        cog = filename[:-3]
        bot.load_extension(f'novabot.cogs.{cog}')
        print(f'{bcolors.WARNING}LOG: "{cog}" cog has been loaded.')

bot.run(token)
