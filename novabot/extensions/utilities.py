from datetime import datetime

import hikari
import lightbulb

utilities = lightbulb.Plugin("Utilities")

@utilities.command
@lightbulb.option("target", "The member to get information about.", hikari.User, required=False)
@lightbulb.command("userinfo", "Get info on a server member")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def userinfo(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.target or ctx.user)

    if not target:
        await ctx.respond("That user is not in the server.")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]

    if roles:
        embed = (
            hikari.Embed(
                title=f"User Info - {target.display_name}",
                description=f"ID: `{target.id}`",
                colour=0x0000ff,
                timestamp=datetime.now().astimezone(),
            )
            .set_footer(
                text=f"Invoked by {ctx.member.display_name}",
                icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
            )
            .set_thumbnail(target.avatar_url or target.default_avatar_url)
            .add_field(
                "Bot?",
                str(target.is_bot),
                inline=True,
            )
            .add_field(
                "Created account on",
                f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
                inline=True,
            )
            .add_field(
                "Joined server on",
                f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
                inline=True,
            )
            .add_field(
                "Roles",
                ", ".join(r.mention for r in roles),
                inline=False,
            )
        )
        
    else:
        embed = (
            hikari.Embed(
                title=f"User Info - {target.display_name}",
                description=f"ID: `{target.id}`",
                colour=0x0000ff,
                timestamp=datetime.now().astimezone(),
            )
            .set_footer(
                text=f"Invoked by {ctx.member.display_name}",
                icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
            )
            .set_thumbnail(target.avatar_url or target.default_avatar_url)
            .add_field(
                "Bot?",
                str(target.is_bot),
                inline=True,
            )
            .add_field(
                "Created account on",
                f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
                inline=True,
            )
            .add_field(
                "Joined server on",
                f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
                inline=True,
            )
        )

    await ctx.respond(embed)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(utilities)