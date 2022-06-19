import disnake  # type: ignore
from disnake.ext import commands  # type: ignore
import datetime


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def help(self,
                   inter: disnake.ApplicationCommandInteraction,
                   module: str = commands.Param(name="module", choices=["Main", "leaderboard", "Info"])):
        """
        Shows helpful information about the bot and how all the commands work.
        """
        embed = disnake.Embed(
            title=f"Help - {module}",
            description=f"Help menu for {module}",
            timestamp=datetime.datetime.now(),
            colour=disnake.Colour.random()
        )
        if module == "Main":
            embed.add_field("Reload", "Reload all files. (LIMITED USERS)")
        elif module == "leaderboard":
            embed.add_field("(slash) setmode", "Set the leaderboard you want to write to.")
            embed.add_field("(slash) add", "Add a leaderboard entry to memory.")
            embed.add_field("(slash) save", "Saves the data in memory to a file (and clears the data).")
            embed.add_field("(slash) showdata", "Shows the recent leaderboard in an embed message.")
        elif module == "Info":
            embed.add_field("help", "shows this menu")
            embed.add_field("invite", "gives a link to invite the bot.")

        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    async def invite(self,
                     inter: disnake.ApplicationCommandInteraction):
        """
        Provides an invite link to the bot.
        """
        button = disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            url="https://discord.com/api/oauth2/authorize?client_id=814582422346792973&permissions=8&scope=bot%20applications.commands",
            label="Invite Me!",
        )

        await inter.response.send_message(components=[button])


def setup(client):
    client.add_cog(Information(client))
