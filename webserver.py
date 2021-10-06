from re import M
from flask import Flask, render_template, request, jsonify
from flask.helpers import make_response
from flask_pymongo import PyMongo
from werkzeug.utils import redirect
from pysteamsignin.steamsignin import SteamSignIn
from datetime import datetime
from helper import *


import json
import requests
import discord_oauth
import webhook
import hashlib
import db_website


from werkzeug.wrappers import response


# TODO remove /discord /steam and only have /link
env = json.load(open("env.json"))

app = Flask(__name__, static_folder='static')
app.config["MONGO_URI"] = env["database"]["database-url"]
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/branding')
def branding():
    return json.load(open("branding.json"))

@app.route('/steam/auth')
def steam_auth():
    hostname = env["webserver"]["webserver-uri"]
    steamLogin = SteamSignIn()
    return steamLogin.RedirectUser(steamLogin.ConstructURL(f"{hostname}/steam"))

@app.route('/steam')
def steam():
    return get_steam_id(mongo)

@app.route('/discord')
def discord():
    return get_discord_id(mongo)

@app.route('/unlink')
async def unlink():
    steam_id, discord_id, discord_username, session = get_cookies()
    resp = make_response(redirect("/link"))
    link = db_website.fetch_link_by_session(mongo, session)
    if link != False:

        db_website.remove_link_from_db(
            mongo, link["discord_id"], link["steam_id"])
        delete_cookies(resp)
        await webhook.unlink_msg(link["discord_id"], link["discord_username"], link["steam_id"])
        return resp
    else:
        return "poof"

@app.route('/link')
async def link():
    steam_id, discord_id, discord_username, session = get_cookies()

    if steam_id != None and discord_id != None and session == None:
        return await add_user_and_render(mongo)
    elif steam_id != None and discord_id != None and session != None:
        return render_template("views/link.html", unlink_url="/unlink", discord_id=discord_id, steam_id=steam_id)

    else:
        return helper_link_check_cookies(steam_id, discord_id, session, env)

@app.route('/settings')
async def settings():
    steam_id, discord_id, discord_username, session = get_cookies()
    
    if session == None and discord_id == None and steam_id == None:
        print("x")
        return redirect("/link")
    else:
        print(session)
        t1, t2, t3, t4 = db_website.fetch_toggles(mongo, session)
        return render_template("views/settings.html", discord_id=discord_id, steam_id=steam_id, togg_1=t1, togg_2=t2, togg_3=t3, togg_4=t4,)

@app.route('/toggle/<id>')
async def toggle(id):
    steam_id, discord_id, discord_username, session = get_cookies()
    if session == None:
        return redirect("/link")
    else:
        db_website.toggle(mongo, session, id)
        return redirect("/settings")


# API
@app.route("/api/<api_key>/<action>")
def api(api_key, action):
    return "WIP"


if __name__ == "__main__":
    devmode = env["webserver"]["webserver-devmode"]

    if devmode:
        app.run(debug=True, host=env["webserver"]["webserver-host"],
                port=env["webserver"]["webserver-port"])

    else:
        from waitress import serve
        serve(app, host=env["webserver"]["webserver-host"],
              port=env["webserver"]["webserver-port"])
