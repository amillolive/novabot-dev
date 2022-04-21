import discord
from discord import slash_command
from discord.ext import commands
from typing import Optional
from novabot import bcolors, GUILD_ID
from datetime import datetime

class Events(commands.Cog, description = 'The events cog. Error handling, guild and member events, and many others are all handled here.'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{bcolors.WARNING}ACTIVE: {self.bot.user} ({self.bot.user.id}) has been marked active.')

def setup(bot):
    bot.add_cog(Events(bot))
