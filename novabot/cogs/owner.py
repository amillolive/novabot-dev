import discord
from discord import slash_command
from discord.ext import commands
from typing import Optional
from novabot import bcolors, GUILD_ID
from datetime import datetime

class Owner(commands.Cog, description='Owner commands. Ony the soul developer of the bot can run these commands.'):
    COG_EMOJI = "👷"
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = 'Close the bot from being active.')
    @commands.is_owner()
    async def close(self, ctx):
        await self.bot.close()

def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))