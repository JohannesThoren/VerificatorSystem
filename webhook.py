from discord import Webhook, RequestsWebhookAdapter
from datetime import datetime
from discord.ext import commands

import json
import discord

env = json.load(open("env.json"))

bot = commands.Bot(command_prefix='#')

intents = discord.Intents.default()
intents.members = True

STEAM_COMMUNITY_URL="https://steamcommunity.com/profiles/"

async def new_user_added(discord_id, discord_username, steam_id): 

    webhook = Webhook.from_url(env["webhook"]["webhook_url"], adapter=RequestsWebhookAdapter())
    guild = webhook.guild
    print(guild)

    embed = discord.Embed(title=f"{discord_username} succesfully verified their accounts!")
    embed.add_field(name="Discord ID", value=discord_id)
    embed.add_field(name="Discord Username", value=discord_username)
    embed.add_field(name="Discord Mention", value=f"<@{discord_id}>")
    embed.add_field(name="Steam ID", value=steam_id)
    embed.add_field(name="Stean Profile", value=f"{STEAM_COMMUNITY_URL}{steam_id}")
    embed.set_footer(text=datetime.now().strftime('%Y-%m-%d %H:%M'))
    webhook.send(embed=embed, username=env["name"]+"-hook")