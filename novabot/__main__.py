import os

import hikari
import lightbulb

from novabot import GUILD_ID, OUTPUT_ID

with open("./secrets/token") as f:
    token = f.read().strip()

bot = lightbulb.BotApp(
    prefix=">",
    intents=hikari.Intents.ALL,
    default_enabled_guilds=GUILD_ID,
    token=token
)

bot.load_extensions_from("./novabot/extensions")

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    print(f"Authenticated as: {bot.get_me()}")
    print("Developed and maintained by vvax#5084")
    await (await bot.rest.fetch_channel(OUTPUT_ID)).send("I'm awake!")

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()
    
    bot.run()