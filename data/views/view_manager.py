import discord
from novabot import BUGREPORT_URL

class BugReportView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label = "Report a bug",
                url = BUGREPORT_URL
            )
        )