import commands
import discord
import json


client = discord.Client()
env = json.load(open("env.json"))

for guild in client.guilds:
    print(guild.name)

@client.event
async def on_ready():
    print("bot is ready")

@client.event
async def on_message(msg):
    if await commands.check_if_msg_is_command(msg):
        print(f"command executed by {msg.author}")

client.run(env["bot"]["discord_bot_token"])