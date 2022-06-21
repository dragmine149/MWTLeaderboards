import disnake  # type: ignore
from disnake.ext import commands  # type: ignore
import datetime


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def help(self,
                   inter: disnake.ApplicationCommandInteraction,
                   module: str = commands.Param(name="module", choices=["Main", "Fun", "leaderboard", "Info"])):
        """
        Shows helpful information about the bot and how all the commands work.
        """
        embed = disnake.Embed(
            title=f"Help - {module}",
            description=f"Help menu for {module}",
            timestamp=datetime.datetime.now(),
            colour=disnake.Colour.random()
        )
        embed.set_footer(text="Prefix = >, slash = /")
        if module == "Main":
            embed.add_field("(prefix) Reload",
                            "Reload all files. (LIMITED USERS)")
        elif module == "Fun":
            embed.add_field("(slash) pong", "Returns bot latency")
            embed.add_field("(prefix) ping", "Returns bot latency")
        elif module == "leaderboard":
            embed.add_field("(slash) setmode",
                            "Set the leaderboard you want to write to.")
            embed.add_field(
                "(slash) add", "Add a leaderboard entry to memory.")
            embed.add_field(
                "(slash) save", "Saves the data in memory to a file (and clears the data).")
            embed.add_field("(slash) showdata",
                            "Shows the recent leaderboard in an embed message.")
            embed.add_field(
                "(slash) requestfile", "Returns the recent leaderboard file (same as showdata but a file instead)")
        elif module == "Info":
            embed.add_field("(slash) help", "shows this menu")
            embed.add_field("(slash) invite",
                            "gives a link to invite the bot.")
            embed.add_field("(slash) updatelog", "Returns the update log")

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

    @commands.slash_command()
    async def updatelog(self,
                        inter: disnake.ApplicationCommandInteraction):
        """
        Shows the update log of the bot
        """
        msg = {
            2: """
            ```
Update 2:
- Fixed an issue with Log breaking the bot before saving file.
- Updated UpdateLog to use a better system
- Removed position argument from add
- Sorted the 'add' list based on the rebirth count
- Fixed an issue with cache length being too long for discord liking
- Removed setmode
- Changed how some files were saved. (Nothing visible, just internal stuff)
- Started progress on wiki conversion. Currently disabled because i can't be bothered to do it atm.
            ```
            """,
            1: """
            ```
Update 1:
- Added request file (get file after save)
- Added update log
- Added automatic roles for ranks.
- Added fun category to help
- Added showcache to see information currently in bot cache.
- Made 'add' only visible to who called it.
            ```
            """,
            0: """
            ```
Update 0:
- Made bot
- Added help, information
- Added setmode, add, save, showdata
- added ping (fun)
            ```
            """
        }
        await inter.response.send_message(msg.get(len(msg) - 1))
        for i in range(len(msg) - 2, -1, -1):
            await inter.channel.send(msg.get(i))


def setup(client):
    client.add_cog(Information(client))
