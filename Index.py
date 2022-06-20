import disnake  # type: ignore
from disnake.ext import commands  # type: ignore
import pickle
import os
from dpyConsole import Console  # type: ignore


# Load discord stuff
intents = disnake.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='>', intents=intents)
my_console = Console(client)


# Send message to console on login.
@client.event
async def on_ready():
    print(f"Logged in as: {client.user}")


# Load cogs and external files
def LoadCogs():
    print("--------------Loading Cogs--------------")
    for cog in os.listdir('./Cogs'):
        if not cog.startswith(".") and not cog.startswith("__"):
            client.load_extension(f"Cogs.{cog[:-3]}")
            print(f"Loaded Cog: {cog}")
    print("--------------Finished Loading Cogs--------------")


def UnLoadCogs():
    print("--------------Unloading Cogs--------------")
    for cog in os.listdir('./Cogs'):
        if not cog.startswith(".") and not cog.startswith("__"):
            try:
                client.unload_extension(f"Cogs.{cog[:-3]}")
            except disnake.ext.commands.errors.ExtensionNotLoaded:
                print(f"Cogs.{cog[:-3]} hasn't been loaded yet.")
    print("--------------Finished Unloading Cogs--------------")


def ReloadCogs():
    print("--------------Reloading Cogs--------------")
    for cog in os.listdir('./Cogs'):
        if not cog.startswith(".") and not cog.startswith("__"):
            try:
                client.reload_extension(f"Cogs.{cog[:-3]}")
                print(f"Reloaded Cog: {cog}")
            except disnake.ext.commands.errors.ExtensionNotLoaded:
                client.load_extension(f"Cogs.{cog[:-3]}")
                print(f"Loaded Cog: {cog} (wasn't loaded beforehand)")
    print("--------------Finished Reloading Cogs--------------")


@client.command()
@commands.is_owner()
async def reload(ctx):
    ReloadCogs()
    await ctx.send("Reloaded cogs!")


# Don't care.
@my_console.command()  # noqa E262
async def reload():  # noqa F811
    ReloadCogs()
    print("Reloaded cogs!")

# Load the bot
LoadCogs()
my_console.start()
os.system("clear")


def getToken():
    token = None
    if not os.path.exists("Token.txt"):
        token = input("Please enter user token: ")
        with open("Token.txt", "wb") as f:
            f.write(pickle.dumps(token))
    else:
        with open("Token.txt", "rb") as f:
            token = pickle.loads(f.read())

    return token


client.run(getToken())
