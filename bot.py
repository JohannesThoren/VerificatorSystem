import re
from discord import member
from pymongo import MongoClient
from discord.ext import commands

import discord
import json

import db_bot

client = discord.Client()
env = json.load(open("env.json"))
bot = commands.Bot(command_prefix=env["app"]["app-bot-prefix"])
mongo = MongoClient(env["database"]["database-url"])[env["app"]["app-name"]]


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
# added some cool stuff
@bot.command(name="discordid", aliases=["DID", "did"])
async def get_link_by_discord_id(ctx, arg):
    if "<" in arg:
        arg = arg.replace("<", "")
        arg = arg.replace(">", "")
        arg = arg.replace("@", "")
        if "!" in arg:
            arg = arg.replace("!", "")

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


@bot.event
async def on_message(msg):
    await bot.process_commands(msg) 

    embeds = msg.embeds
    embed_dict = ""
    do_reaction =  env["app"]["app-react-on-webhook"]
    

    if msg.author.name == env["app"]["app-name"]+"-hook":
        for embed in embeds:
            embed_dict = embed.to_dict()

        role = discord.utils.get(msg.guild.roles, name=env["app"]["app-role-name"])
        user = await msg.guild.fetch_member(int(embed_dict["fields"][0]["value"]))
        if embed_dict["title"] == "Linked!":
            await user.add_roles(role)
            

        elif embed_dict["title"] == "Unlinked!":
            await user.remove_roles(role)
            

        if do_reaction:
            await msg.add_reaction("✅")
            


bot.run(env["app"]["app-token"])