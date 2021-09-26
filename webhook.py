from discord import Webhook, RequestsWebhookAdapter

import json
import discord

env = json.load(open("env.json"))
webhook = Webhook.from_url(env["webhook"]["webhook_url"], adapter=RequestsWebhookAdapter())

def new_user_added(discord_id): 
    return