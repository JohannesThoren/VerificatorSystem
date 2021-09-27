from flask import Flask, render_template, request, jsonify
from flask.helpers import make_response
from flask_pymongo import PyMongo
from werkzeug.utils import redirect
from pysteamsignin.steamsignin import SteamSignIn
from datetime import datetime

import json
import requests
import discord_oauth
import webhook
import hashlib
import db_website

from werkzeug.wrappers import response


#TODO remove /discord /steam and only have /link 
env = json.load(open("env.json"))

app = Flask(__name__, static_folder='static')
app.config["MONGO_URI"] = env["db"]["url"]
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/discord')
def discord():
    code = request.args.get("code")
    if code:
        token = discord_oauth.get_access_token(code)["access_token"]
        user = discord_oauth.get_user(token)
        
        resp = make_response(redirect("/link"))
        resp.set_cookie("discord_id", value=user["id"])
        resp.set_cookie("discord_username", value=user["username"]) 

        print(user)
        return resp
    else:
        return render_template("views/discord.html", discord_url = env["oauth_discord"]["sign_in_url"])

@app.route('/steam/auth')
def auth_steam():
    hostname = "http://"+env["webserver"]["hostname"]+":"+str(env["webserver"]["port"])
    steamLogin = SteamSignIn()
    return steamLogin.RedirectUser(steamLogin.ConstructURL(f"{hostname}/steam"))
  

@app.route('/steam')
def steam():
    user = request.args.get("openid.identity")
    if user:
        parts = user.split("/")
        id = parts[len(parts) -1 ]
        resp = make_response(redirect("/link"))
        resp.set_cookie("steam_id", value=id)

        return resp 
    else:
        return render_template("views/steam.html", steam_url="/steam/auth")


@app.route('/link/<session>')
def recover_link(session):
    return

# gör så att man hamnar på link sidan.
# FUNKTIONER
# - är steam och discord länkat, visa det
# - är de inte länkade ta användare till en sida för att länka sina konton
@app.route('/link')
async def link():
    steam_id = request.cookies.get("steam_id")
    discord_id = request.cookies.get("discord_id")
    discord_username = request.cookies.get("discord_username")
    session = request.cookies.get("session")

    print(steam_id)

    if discord_id == None:
        return make_response(redirect("/discord"))
    elif steam_id == None:
        return make_response(redirect("/steam"))
    elif session != None:
        return "poof"
    else:
        resp = make_response(render_template("views/link.html", discord_id=discord_id, steam_id=steam_id))
        resp.delete_cookie("discord_id")
        resp.delete_cookie("discord_username")
        resp.delete_cookie("steam_id")

        tmp_session = hashlib.md5(str(str(steam_id)+str(discord_id)+str(datetime.now().strftime('%Y-%m-%d %H:%M'))).encode("UTF-8")).hexdigest()
        resp.set_cookie("session", tmp_session)

        # TODO add a "add to database" function

        if db_website.add_link_to_db(mongo, tmp_session, discord_id, steam_id, discord_username):
            await webhook.new_user_added(discord_id, discord_username, steam_id)
        
        return resp



if __name__ == "__main__":
    app.run(debug=True, host=env["webserver"]["host"], port=env["webserver"]["port"])