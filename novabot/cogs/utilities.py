import discord
from discord import slash_command, Option
from discord.ext import commands, pages
from typing import Optional
from novabot import bcolors, GUILD_ID, NBRoleConverter, APP_ID, command_help
from datetime import datetime
import asyncio
import os
import sqlite3 as sql

class Utilities(commands.Cog, description='All utility commands. Utility commands are similar to the usefulness of moderation commands without the permission requirements needed.'):
    COG_EMOJI = "🛠️"
    def __init__(self, bot):
        self.bot = bot
    
    cog_command_help = command_help["utilities"]
    
    @commands.command(aliases = (['latency']), help = cog_command_help["ping"], description = 'Check the latency of the bot.')
    @commands.cooldown(1, 3.0, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(
            title = 'Pong!',
            colour = self.bot.default_colour,
            description = f'My latency is roughly `{round(self.bot.latency * 1000)}ms`.'
        )
        embed.set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @slash_command(help = cog_command_help["ping"], name = 'ping', description = 'Check the latency of the bot.', guild_ids = [GUILD_ID])
    async def _ping(self, ctx):
        embed = discord.Embed(
            title = 'Pong!',
            colour = self.bot.default_colour,
            description = f'My latency is roughly `{round(self.bot.latency * 1000)}ms`.'
        )
        embed.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)

        await ctx.respond(embed = embed, ephemeral = True)

    @commands.command(help = cog_command_help["members"], description = 'Get a list of members in a role.')
    @commands.guild_only()
    @commands.cooldown(1, 3.0, commands.BucketType.member)
    async def members(self, ctx, *, role : NBRoleConverter):
        embeds = []

        fields = 0

        current = discord.Embed(
            title = f'Members in {role}',
            description = f"`{len(role.members)} members total.`",
            colour = self.bot.default_colour
        )
        current.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
        current.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)

        for member in role.members:
            fields += 1
            if fields == 25:
                embeds.append(current)
                current = discord.Embed(
                    title = f'Members in {role}',
                    description = f"`{len(role.members)} members total.`",
                    colour = self.bot.default_colour
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
                    description = f'`No members were found in {role}.`',
                    colour = self.bot.default_colour
                )
                embed.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
                embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)

                await ctx.reply(embed = embed)
                return
            embeds.append(current)
        
        paginator = pages.Paginator(pages = embeds)
        await paginator.send(ctx)

    @slash_command(name = 'members', description = 'Get a list of members in a role.', guild_ids = [GUILD_ID])
    async def _members(self, ctx, *, role: Option(discord.Role, "The role to gather members from.", required = True)):
        embeds = []

        fields = 0

        current = discord.Embed(
            title = f'Members in {role}',
            description = f"`{len(role.members)} members total.`",
            colour = self.bot.default_colour
        )
        current.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
        current.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)

        for member in role.members:
            fields += 1
            if fields == 25:
                embeds.append(current)
                current = discord.Embed(
                    title = f'Members in {role}',
                    description = f"`{len(role.members)} members total.`",
                    colour = self.bot.default_colour
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
                    description = f'`No members were found in {role}.`',
                    colour = self.bot.default_colour
                )
                embed.set_footer(text = self.bot.user.display_name, icon_url = self.bot.user.display_avatar.url)
                embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)

                await ctx.reply(embed = embed)
                return
            embeds.append(current)
        
        paginator = pages.Paginator(pages = embeds)
        await paginator.respond(ctx.interaction, ephemeral = True)

def setup(bot):
    bot.add_cog(Utilities(bot))
