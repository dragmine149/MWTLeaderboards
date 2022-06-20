import disnake  # type: ignore
from disnake.ext import commands  # type: ignore
import os
import datetime


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mode = None
        self.data = {}
        # self.__testMode()

    def __testMode(self):
        self.mode = "Test"
        self.data = {
            1: {
                "name": "dragmine149",
                "value": 10
            }
        }

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

    def __sortDict(self, dict):
        arr = []
        Index = 0
        print(len(dict))
        for item in dict:
            dictItem = dict[item]
            print(len(arr))
            if len(arr) == 0:
                arr.append(dictItem)
                Index = arr.index(dictItem)
                continue

            for arrItem in arr:
                if arrItem["value"] > dictItem["value"]:
                    # Index = arr.index(arrItem)
                    continue
                if arrItem["value"] == dictItem["value"]:
                    # Index = arr.index(arrItem)
                    continue
                if arrItem["value"] < dictItem["value"]:
                    Index = arr.index(arrItem)
                    arr.insert(Index, dictItem)
                    Index = arr.index(dictItem)
                    break

        print(Index)
        for arrItem in arr:
            arrItem["position"] = arr.index(arrItem) + 1

        for item in arr:
            dict[item["position"] - 1] = item

        return dict, Index

    @commands.slash_command()
    async def add(self,
                  inter: disnake.ApplicationCommandInteraction,
                  name: str,
                  value: int):
        """
        Adds the user data to an array.

        Parameters
        ----------
        name (string): The username of the person
        value (int): The ammount of X the user has.
        """
        position = len(self.data)

        self.data[position] = {"position": position,
                               "name": name, "value": value}
        newdata = {}
        for item in sorted(self.data):
            newdata[item] = self.data[item]

        self.data = newdata
        await inter.response.send_message(f"Added field: {self.data[position]}", ephemeral=True)  # noqa E501
        self.data, Index = self.__sortDict(self.data)
        originalMessage = await inter.original_message()
        print(Index)
        print(self.data)
        await originalMessage.edit(f"Added field: {self.data[Index]}")  # noqa E501

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

    def __getRole(self):
        roleId = {
            "Most Rebirths": None,
            "Most Kills": None,
            "Reseting Rebirths": 988212587760087071,
            "Reseting Kills": 988211618259288080,
            "Test": None
        }
        return roleId.get(self.mode)

    @commands.slash_command()
    async def save(self,
                   inter: disnake.ApplicationCommandInteraction):
        """
        Saves the data and sends a file
        """
        # Tests
        if self.mode is None:
            await inter.response.send_message("Please specifi a mode using `/setmode`!")  # noqa E501
            return

        if len(self.data) == 0:
            await inter.response.send_message("Please enter some data using `/add`")  # noqa E501
            return

        # Give role
        members = inter.guild.fetch_members()
        roleId = self.__getRole()
        Log = ""
        if roleId is not None:
            role = inter.guild.get_role(roleId)
            async for member in members:
                name = member.display_name
                if member.get_role(roleId) is not None:
                    await member.remove_roles(role, reason="Leaderboard update, Reseting...")
                    Log += f"Remove {member.mention} '{role.mention}'\n"

                if name == self.data[1]["name"]:
                    await member.add_roles(role, reason=f"Top of leaderboard for {self.mode}")
                    Log += f"Gave {member.mention} '{role.mention}'\n"
        else:
            Log += f"No role id assaigned for {self.mode}"

        # Saves files
        dataString = f"{self.mode} leaderboard\n\n"
        for index in self.data:
            value = self.data[index]["value"]
            name = self.data[index]["name"]
            end = self.__generateEnd(value)
            dataString += f"{index}{end} {name} - {value}, "

        with open(f"Files/{self.mode}-data.txt", "w+") as file:
            file.write(dataString)

        with open(f"Files/{self.mode}-json.txt", "w+") as file:
            file.write(self.data)

        self.data = {}  # reset cache

        file = disnake.File(f"Files/{self.mode}-Data.txt", f"{self.mode} leaderboard.txt", description=f"{self.mode} leaderboard for this week.")  # noqa E501
        await inter.response.send_message("Here is your file: ", file=file)
        if Log != "":
            await inter.channel.send(f"Log:\n{Log}")

    @commands.slash_command()
    async def showcache(self,
                        inter: disnake.ApplicationCommandInteraction):
        """
        Shows what is currently in the bot cache
        """
        cache = f"Data: {self.data}\nMode: {self.mode}"
        await inter.response.send_message(cache)

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

    @commands.slash_command()
    async def requestfile(self,
                          inter: disnake.ApplicationCommandInteraction,
                          mode: str = commands.Param(name="mode", choices=["Most Rebirths", "Most Kills", "Reseting Rebirths", "Reseting Kills"])):
        """
        Returns the file of the selected mode
        """
        try:
            file = disnake.File(f"Files/{mode}-Data.txt", f"{mode} leaderboard.txt", description=f"{mode} leaderboard for this week.")  # noqa E501
            await inter.response.send_message("Here is your file: ", file=file)
        except FileNotFoundError:
            await inter.response.send_message("No data has been recorded for this leaderboard yet!")


def setup(client):
    client.add_cog(Leaderboard(client))
