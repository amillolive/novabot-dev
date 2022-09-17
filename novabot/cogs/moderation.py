import discord
from discord import slash_command
from discord.ext import commands
from typing import Optional
from novabot import bcolors, GUILD_ID, NBRoleConverter, APP_ID
from datetime import datetime
import asyncio
import os
import sqlite3 as sql

class Moderation(commands.Cog, description='All moderation commands. Bans, mutes, kicks, they are all handled here.'):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Moderation(bot))
