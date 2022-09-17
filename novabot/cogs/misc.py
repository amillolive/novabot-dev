import discord
from discord import slash_command, Option
from discord.ext import commands
from discord.commands import permissions
from typing import Optional, Union
from novabot import bcolors, GUILD_ID, NBRoleConverter, APP_ID, start_db, close_db, command_help
from datetime import datetime
import asyncio
import os
import sqlite3 as sql

class Misc(commands.Cog, description="All commands that don't fall into a specific category."):
    COG_EMOJI = "🛡️"
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Misc(bot))
