import discord
from discord import slash_command
from discord.ext import commands
from typing import Optional
from novabot import bcolors, GUILD_ID, start_db, close_db
from datetime import datetime
import traceback
import sys
from data.views.view_manager import BugReportView
import sqlite3 as sql
class Events(commands.Cog, description = 'The events cog. Error handling, guild and member events, and many others are all handled here.'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{bcolors.WARNING}ACTIVE: {self.bot.user} ({self.bot.user.id}) has been marked active.')
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        
        ignored = (commands.CommandNotFound)

        error = getattr(error, 'original', error)
    
        if isinstance(error, ignored):
            return
        
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title = 'Oh no!',
                colour = self.bot.default_colour,
                description = f"A bad argument was provided."
            )
            embed.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
            embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)

            await ctx.send(embed = embed, view = BugReportView())

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        
        ignored = (commands.CommandNotFound)

        error = getattr(error, 'original', error)
    
        if isinstance(error, ignored):
            return

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db, c = await start_db()

        c.execute(f"SELECT * FROM main WHERE guild_id = {guild.id}")
        result = c.fetchone()

        if result is None:
            sqldata = ("INSERT INTO main(guild_id, mod_id, log_id, prefix, owner_id) VALUES(?, ?, ?, ?, ?)")
            vals = (guild.id, None, None, ">", guild.owner.id)
            c.execute(sqldata, vals)
        
        db.commit()

        await close_db(db, c)

def setup(bot):
    bot.add_cog(Events(bot))
