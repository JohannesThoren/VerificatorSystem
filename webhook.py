from discord import Webhook, RequestsWebhookAdapter
from datetime import datetime
from discord.ext import commands

import json
import discord

env = json.load(open("env.json"))

bot = commands.Bot(command_prefix='#')

intents = discord.Intents.default()
intents.members = True

STEAM_COMMUNITY_URL = "https://steamcommunity.com/profiles/"


def embed(discord_username, discord_id, steam_id, prefix, action, color):

    embed = discord.Embed(
        title=f"{prefix}!", description=f"{discord_username} successfully {action} their account!", color=color)
    embed.add_field(name="Discord ID", value=discord_id)
    embed.add_field(name="Discord Username", value=discord_username)
    embed.add_field(name="Discord Mention", value=f"<@{discord_id}>")
    embed.add_field(name="Steam ID", value=steam_id)
    embed.add_field(name="Steam Profile",
                    value=f"{STEAM_COMMUNITY_URL}{steam_id}")
    embed.set_footer(text=datetime.now().strftime('%Y-%m-%d %H:%M'))

    return embed


async def new_user_added(discord_id, discord_username, steam_id):

    webhook = Webhook.from_url(
        env["app"]["app-webhook-url"], adapter=RequestsWebhookAdapter())

    webhook.send(embed=embed(discord_username, discord_id,
                 steam_id, "Linked", "verified", 0x00ff00), username=env["app"]["app-name"]+"-hook")


async def unlink_msg(discord_id, discord_username, steam_id):
    webhook = Webhook.from_url(
        env["app"]["app-webhook-url"], adapter=RequestsWebhookAdapter())

    webhook.send(embed=embed(discord_username, discord_id,
                 steam_id, "Unlinked", "unlinked", 0xff0000), username=env["app"]["app-name"]+"-hook")
