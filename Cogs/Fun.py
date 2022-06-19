import disnake
from disnake.ext import commands  # type: ignore
import random


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    def __messages(self, input="Pong"):
        result = random.randint(0, 400)
        switch = {
            0: f"{input}! {round(self.client.latency * 1000)}ms",
            100: "Oops, you hit the net... 1 point to me.",
            200: "Well done, i missed... 1 point to you.",
            300: "Erm, where did that ball go? Reset?",
            400: "What am i doing? Why am i here?"
        }
        msg = switch.get(result)
        if msg is None:
            msg = switch.get(0)
        return msg, result

    @commands.command()
    async def ping(self, ctx):
        msg, result = self.__messages()
        await ctx.send(f"{msg} ({result})")

    @commands.slash_command(
        description="Returns the bot latency",
        guild_ids=[686177483430952970])
    async def pong(self, inter: disnake.ApplicationCommandInteraction):
        msg, result = self.__messages("Ping")
        await inter.response.send_message(f"{msg} ({result})")


def setup(client):
    client.add_cog(Fun(client))
