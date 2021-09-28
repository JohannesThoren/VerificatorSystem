from pymongo import MongoClient
from discord.ext import commands

import discord
import json

import db_bot

client = discord.Client()
env = json.load(open("env.json"))
bot = commands.Bot(command_prefix=env["bot"]["prefix"])
mongo = MongoClient(env["db"]["url"])[env["name"]]


def link_embed(link):
    STEAM_COMMUNITY_URL="https://steamcommunity.com/profiles/"
    discord_username = link["discord_username"]
    discord_id = link["discord_id"]
    steam_id = link["steam_id"]

    embed = discord.Embed(title=f"{discord_username}'s steam link")
    embed.add_field(name="Discord ID", value=discord_id)
    embed.add_field(name="Discord Username", value=discord_username)
    embed.add_field(name="Discord Mention", value=f"<@{discord_id}>")
    embed.add_field(name="Steam ID", value=steam_id)
    embed.add_field(name="Stean Profile", value=f"{STEAM_COMMUNITY_URL}{steam_id}")
    
    return embed

@bot.command(name="discordid", aliases=["DID", "did"])
async def get_link_by_discord_id(ctx, arg):

    link = db_bot.fetch_link_by_discord_id(mongo, arg)
    embed = discord.Embed()

    if link:
        await ctx.channel.send(embed=link_embed(link))
    
    else:
        await ctx.channel.send("could not find anyone with that discord id...")

@bot.command(name="steamid", aliases=["SID", "sid"])
async def get_link_by_steam_id(ctx, arg):
    link = db_bot.fetch_link_by_steam_id(mongo, arg)
    embed = discord.Embed()

    if link:
        await ctx.channel.send(embed=link_embed(link))
    
    else:
        await ctx.channel.send("could not find anyone with that steam id...")


for guild in client.guilds:
    print(guild.name)

@client.event
async def on_ready():
    print("bot is ready")

bot.run(env["bot"]["discord_bot_token"])