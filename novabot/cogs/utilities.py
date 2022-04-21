import discord
from discord import slash_command
from discord.ext import commands
from typing import Optional
from novabot import bcolors, GUILD_ID, NBRoleConverter
from datetime import datetime
import Paginator

class Utilities(commands.Cog, description='All utility commands. Utility commands are similar to the usefulness of moderation commands without the requirements needed.'):
    COG_EMOJI = "🛠️"
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(description = 'Check the latency of the bot.')
    async def ping(self, ctx):
        embed = discord.Embed(
            title = 'Pong!',
            colour = self.bot.default_colour,
            description = f'My latency is roughly `{round(self.bot.latency * 1000)}ms`.'
        )
        embed.set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @slash_command(name = 'ping', description = 'Check the latency of the bot.', guild_ids = [GUILD_ID])
    async def _ping(self, ctx):
        await ctx.defer()

        embed = discord.Embed(
            title = 'Pong!',
            colour = self.bot.default_colour,
            description = f'My latency is roughly `{round(self.bot.latency * 1000)}ms`.'
        )
        embed.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
        embed.set_author(name=ctx.author.display_name, icon_url = ctx.author.display_avatar.url)

        await ctx.respond(embed=embed)

    @commands.command(description = 'Get a list of members in a role.')
    async def members(self, ctx, *, role : NBRoleConverter):
        embeds = []

        fields = 0

        current = discord.Embed(
            title = f'List of members in {role}',
            description = f"`{self.bot.user.display_name}'s advanced command manager.`",
            colour = self.bot.default_colour
        )
        current.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
        current.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)

        for member in role.members:
            fields += 1
            if fields == 25:
                embeds.append(current)
                current = discord.Embed(
                    title = f'List of members in {role}',
                    description = f"`{self.bot.user.display_name}'s advanced command manager.`",
                    colour = self.bot.default_color
                )
                current.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
                current.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)
                fields = 0
                continue
            current.add_field(name=f'{member.top_role}', value=f'`Member:` {member.mention} \n `Tag:` {member}', inline=True)

        if not embeds:
            if not current.fields:
                embed = discord.Embed(
                    title = 'No members found',
                    description = f'No members were found in {role}.',
                    colour = self.bot.utils_color
                )
                embed.set_footer(text = f'Invoked by {ctx.author.name}.')

                if ctx.guild.icon:
                    embed.set_author(name = f'{ctx.guild}', icon_url=f'{ctx.guild.icon.url}')
                else:
                    embed.set_author(name = f'{ctx.guild}', icon_url=f'{ctx.author.display_avatar.url}')

                embed.set_thumbnail(url = f'{self.bot.user.display_avatar.url}')

                await ctx.reply(embed = embed)
                return
            embeds.append(current)
        
        await Paginator.Simple().start(ctx, pages = embeds)

def setup(bot):
    bot.add_cog(Utilities(bot))