import disnake  # type: ignore
from disnake.ext import commands  # type: ignore
import os
import datetime


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mode = None
        self.data = {}

    @commands.slash_command()
    async def setmode(self,
                      inter: disnake.ApplicationCommandInteraction,
                      mode: str = commands.Param(name="mode", choices=["Most Rebirths", "Most Kills", "Reseting Rebirths", "Reseting Kills"])):  # noqa E501
        """
        Sets the mode of the leaderboard for the data to record.

        Paramaters
        ----------
        mode: The mode to record the data.
        """
        self.mode = mode
        await inter.response.send_message(f"Changed mode to {mode}")

    @commands.slash_command()
    async def add(self,
                  inter: disnake.ApplicationCommandInteraction,
                  position: commands.Range[0, 75],
                  name: str,
                  value: int):
        """
        Adds the user data to an array.

        Parameters
        ----------
        position (int): The position on the leaderboard
        name (string): The username of the person
        value (int): The ammount of X the user has.
        """
        self.data[position] = {"name": name, "value": value}
        await inter.response.send_message(f"Added field: {self.data[position]}")  # noqa E501

    def __generateEnd(self, value):
        ends = {
            0: "th",
            1: "st",
            2: "nd",
            3: "rd"
        }
        hunRem = value % 100  # divisble by 100
        tenRem = value % 10  # divisible by 10

        if (hunRem - tenRem == 10):
            return ends.get(0)

        result = ends.get(tenRem)
        if result is None:
            result = ends.get(0)
        return result

    @commands.slash_command()
    async def save(self,
                   inter: disnake.ApplicationCommandInteraction):
        """
        Saves the data and sends a file
        """
        if self.mode is None:
            await inter.response.send_message("Please specifi a mode using `/setmode`!")  # noqa E501
            return

        if len(self.data) == 0:
            await inter.response.send_message("Please enter some data using `/add`")  # noqa E501
            return

        dataString = f"{self.mode} leaderboard\n\n"
        for index in self.data:
            value = self.data[index]["value"]
            name = self.data[index]["name"]
            end = self.__generateEnd(value)
            dataString += f"{index}{end} {name} - {value}, "

        with open(f"Files/{self.mode}-data.txt", "w+") as file:
            file.write(dataString)

        file = disnake.File(f"Files/{self.mode}-Data.txt", f"{self.mode} leaderboard.txt", description=f"{self.mode} leaderboard for this week.")  # noqa E501
        await inter.response.send_message("Here is your file: ", file=file)

    @commands.slash_command()
    async def showdata(self,
                       inter: disnake.ApplicationCommandInteraction,
                       mode: str = commands.Param(name="mode", choices=["Most Rebirths", "Most Kills", "Reseting Rebirths", "Reseting Kills"])):
        """
        Returns an embed of the recent leaderboard.

        Paramaters
        ----------
        mode: Leaderboard you want the data of
        """
        if mode is None:
            mode = self.mode

        if not os.path.exists(f"Files/{mode}-data.txt"):
            await inter.response.send_message(f"Couldn't find data for {mode}!")
            return

        data = None
        with open(f"Files/{mode}-data.txt", "r") as file:
            data = file.read()
        editedTime = os.path.getmtime(f"Files/{mode}-data.txt")

        embed = disnake.Embed(
            title=f"{mode} leaderboard",
            description="The recent leaderboard.",
            timestamp=datetime.datetime.fromtimestamp(editedTime),
            colour=disnake.Colour.random()
        )
        data = data.split("\n")[2:][0]
        userData = data.split(", ")

        for user in userData:
            # Skip if empty
            if user.rstrip() == "":
                continue

            # Transalte to embed field
            userInfo = user.split(" ")
            print(userInfo)
            embed.add_field(f"{userInfo[0]} - {userInfo[1]}", userInfo[3])

        await inter.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Leaderboard(client))
