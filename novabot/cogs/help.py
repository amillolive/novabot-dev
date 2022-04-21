import discord
from discord import slash_command
from discord.ext import commands
from typing import Optional
from novabot import bcolors, GUILD_ID
from datetime import datetime

class HelpDropdown(discord.ui.Select):
    def __init__(self, help_command: "NovaBotHelpCommand", options: list[discord.SelectOption]):
        super().__init__(placeholder = "Choose a category...", min_values = 1, max_values = 1, options = options)
        self.help_command = help_command
    
    async def callback(self, interaction: discord.Interaction):
        embed = (
            await self.help_command.cog_help_embed(self.help_command.context.bot.get_cog(self.values[0]))
            if self.values[0] != self.options[0].value 
            else await self.help_command.bot_help_embed(self.help_command.get_bot_mapping())
        )
        await interaction.response.edit_message(embed = embed)

class HelpView(discord.ui.View):
    def __init__(self, help_command: "NovaBotHelpCommand", options: list[discord.SelectOption], *, timeout: Optional[float] = 120.0):
        super().__init__(timeout = timeout)
        self.add_item(HelpDropdown(help_command, options))
        self.help_command = help_command
        
    async def on_timeout(self) -> None:
        self.clear_items()
        await self.help_command.response.edit(content='Timed out.', view=self)
        

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.help_command.context.author == interaction.user
        

class NovaBotHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'
    
    async def cog_select_options(self) -> list[discord.SelectOption]:
        options: list[discord.SelectOption] = []
        options.append(
            discord.SelectOption(
                label = "Main",
                emoji = "🏠",
                description = "Go back to he main page."
            )
        )
        
        for cog, command_set in self.get_bot_mapping().items():
            filtered = await self.filter_commands(command_set, sort=True)

            if not filtered:
                continue

            emoji = getattr(cog, "COG_EMOJI", None)

            options.append(
                discord.SelectOption(
                    label=cog.qualified_name if cog else "No Category",
                    emoji=emoji,
                    description=cog.description[:100] if cog and cog.description else None
                )
            )
        return options
    
    async def help_embed(
        self, 
        title: str, 
        description: Optional[str] = None, 
        mapping: Optional[str] = None,
        command_set: Optional[set[commands.Command]] = None
    ) -> discord.Embed:
        embed = discord.Embed(
            title = title,
            description = f'Use `{self.context.clean_prefix}help [command]` for more information on a command.\nYou can also use `{self.context.clean_prefix}help [category]` for more information on a category.' if not description else description,
            colour = discord.Colour.from_rgb(r=0, g=0, b=255),
        )
        embed.set_footer(text="NovaBot's help assistant.", icon_url=self.context.bot.user.display_avatar.url)
        embed.set_author(name=self.context.author.display_name, icon_url=self.context.author.display_avatar.url)
        
        if command_set:
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                embed.add_field(name = self.get_command_signature(command), value = command.description or 'N/A', inline = False)

        elif mapping:
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "No Category"
                cmd_list = f"\n".join(f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered)
                value = (
                    f"*{cog.description}*\n{cmd_list}" if cog and cog.description else cmd_list
                )
                embed.add_field(name=name, value=value)

        return embed
    
    async def send_bot_help(self, mapping: dict):
        embed = await self.bot_help_embed(mapping)
        options = await self.cog_select_options()
        self.response = await self.get_destination().send(embed=embed, view=HelpView(self, options))
    
    async def bot_help_embed(self, mapping: dict) -> discord.Embed:
        embed = await self.help_embed(
            title = 'Help Assistant (home)',
            mapping = mapping
        )
        return embed

    async def send_command_help(self, command: commands.Command):
        embed = await self.help_embed(
            title = 'Help Assistant (command)',
            command_set = commands.command if isinstance(command, commands.Group) else None
        )
        embed.add_field(name = f'{self.context.clean_prefix}{command.qualified_name}', value = f'{command.help}')
        await self.get_destination().send(embed=embed)        

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self.cog_help_embed(cog)
        await self.get_destination().send(embed=embed)
    
    send_group_help = send_command_help

    async def cog_help_embed(self, cog: commands.Cog) -> discord.Embed:
        embed = await self.help_embed(
            title = 'Help Assistant (cog)',
            command_set = cog.get_commands()
        )
        try:
            embed.add_field(name = f'{cog.qualified_name}', value = f'{cog.description}')
        except:
            embed.add_field(name = f'{cog.qualified_name}', value = 'N/A')
        return embed

    async def send_error_message(self, error):
        print(f"{bcolors.FAIL}ERROR: {error}")
        embed = await self.help_embed(
            title = 'Error Found',
            description = f'`{error}`'
        )
        channel = self.get_destination()
        await channel.send(embed=embed)

class Help(commands.Cog, description="The help command. A single command that can be used to navigate and learn about all the commands in NovaBot's arsenal."):
    COG_EMOJI = "❓"
    def __init__(self, bot):
        self.bot = bot
        
        self._original_help_command = bot.help_command
        bot.help_command = NovaBotHelpCommand()
        bot.help_command.cog = self

def setup(bot):
    bot.add_cog(Help(bot))