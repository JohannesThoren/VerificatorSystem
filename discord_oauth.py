import json
import requests
from werkzeug.datastructures import Authorization

from werkzeug.utils import redirect
from werkzeug.wrappers import request
env = json.load(open("env.json"))

CLIENT_ID = env["oauth_discord"]["client_id"]
SECRET = env["oauth_discord"]["client_secret"]
DISCORD_API_BASE_URL = "https://discord.com/api"
DISCORD_SIGN_IN_URL = env["oauth_discord"]["sign_in_url"]
DISCORD_REDIRECT_URI = env["oauth_discord"]["redirect_uri"]
DISCORD_OAUTH_SCOPE = env["oauth_discord"]["scope"]
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"


def get_access_token(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": DISCORD_OAUTH_SCOPE
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    req = requests.post(f"{DISCORD_API_BASE_URL}/oauth2/token", data=data, headers=headers)

    return req.json()

def get_user(access_token):

    headers = {
        "Authorization": "Bearer {}".format(access_token)
    }

    req = requests.get(f"{DISCORD_API_BASE_URL}/users/@me", headers=headers)

    return req.json()