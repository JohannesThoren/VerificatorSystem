import json
env = json.load(open("env.json"))


DISCORD_API_BASE_URL = "https://discordapp.com/api"
DISCORD_REDIRECT_URI = env["webserver"]["hostname"]+":"+str(env["webserver"]["port"])