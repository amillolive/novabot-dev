import discord
from discord import slash_command
from discord.ext import commands
from typing import Optional
from novabot import bcolors, GUILD_ID, NBRoleConverter, APP_ID
from datetime import datetime
import asyncio
import os
import sqlite3 as sql        

class NovaBotHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    
    def get_command_signature(self, command):
        return f'`{self.context.clean_prefix}{command.name}` `{command.signature}`'
    
    def get_command_aliases(self, command):
        if not command.aliases:
            return 'There are no aliases for this command currently.'
        else:
            return f'[`{"` | `".join([alias for alias in command.aliases])}`]'
        
    def get_command_help(self, command):
        if not command.help:
            return 'There is no documentation for this command currently.'
        else:
            return command.help
        
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title = 'Help Assistant',
            description = 'Shows important information on how to use commands.',
            colour = self.context.bot.default_colour
        )
        embed.set_author(name = f'{self.context.bot.user.name}', icon_url = f'{self.context.bot.user.display_avatar}')
        embed.set_footer(text = f"{self.context.bot.user.name}'s Help Assistant", icon_url = f'{self.context.bot.user.display_avatar}')

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort = True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name = f'{cog_name}', value = "\n".join(command_signatures), inline = True)
        
        channel = self.get_destination()
        await channel.send(embed = embed)
    
    async def send_command_help(self, command):
        embed = discord.Embed(
            title = 'Help Assistant',
            description = f'{self.get_command_signature(command)}',
            colour = self.context.bot.default_colour
        )
        embed.set_author(name = f'{self.context.bot.user.name}', icon_url = f'{self.context.bot.user.display_avatar}')
        embed.set_footer(text = f"{self.context.bot.user.name}'s Help Assistant", icon_url = f'{self.context.bot.user.display_avatar}')
        
        embed.add_field(name = 'Aliases', value = f"{self.get_command_aliases(command)}", inline = False)
        embed.add_field(name = 'Command Help', value = f"{self.get_command_help(command)}", inline =  False)
        
        channel = self.get_destination()
        await channel.send(embed = embed)
    
    async def send_group_help(self, group):
        embed = discord.Embed(
            title = 'Help Assistant',
            description = f'`{group.qualified_name}`',
            colour = self.context.bot.default_colour
        )
        embed.set_author(name = f'{self.context.bot.user.name}', icon_url = f'{self.context.bot.user.display_avatar}')
        embed.set_footer(text = f"{self.context.bot.user.name}'s Help Assistant", icon_url = f'{self.context.bot.user.display_avatar}')

        commands = group.commands
        filtered = await self.filter_commands(commands, sort = True)
        command_signatures = [self.get_command_signature(c) for c in filtered]

        if command_signatures:
            embed.add_field(name = f'Subcommands', value = "\n".join(command_signatures), inline = True)
        
        channel = self.get_destination()
        await channel.send(embed = embed)
    
    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title = 'Help Assistant',
            description = f'__**{cog.qualified_name}**__: {cog.description}',
            colour = self.context.bot.default_colour
        )
        embed.set_author(name = f'{self.context.bot.user.name}', icon_url = f'{self.context.bot.user.display_avatar}')
        embed.set_footer(text = f"{self.context.bot.user.name}'s Help Assistant", icon_url = f'{self.context.bot.user.display_avatar}')
        
        commands = cog.get_commands()
        filtered = await self.filter_commands(commands, sort = True)
        command_signatures = [self.get_command_signature(c) for c in filtered]
        
        if command_signatures:
            embed.add_field(name = f'Cog Commands', value = "\n".join(command_signatures), inline = True)
        
        channel = self.get_destination()
        await channel.send(embed = embed)

class Help(commands.Cog, description="The help command. A single command that can be used to navigate and learn about all the commands in NovaBot's arsenal."):
    COG_EMOJI = "❓"
    def __init__(self, bot):
        self.bot = bot
        
        self._original_help_command = bot.help_command
        bot.help_command = NovaBotHelpCommand()
        bot.help_command.cog = self

def setup(bot):
    bot.add_cog(Help(bot))