# Helper functions for the routes
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

def helper_link_check_cookies(steam_id, discord_id, session, env):

    if steam_id != None and discord_id == None:
        return render_template("views/link.html", discord_url=env["app"]["app-oauth-url"], steam_id=steam_id, discord_id="[Not Linked]")

    elif steam_id == None and discord_id != None:
        return render_template("views/link.html", steam_url="/steam/auth", discord_id=discord_id, steam_id="[Not Linked]")

    elif steam_id == None and discord_id == None:
        return render_template("views/link.html", steam_url="/steam/auth", discord_url=env["app"]["app-oauth-url"], steam_id="[Not Linked]", discord_id="[Not Linked]")
    elif session != None:
        return render_template("views/link.html")

def get_cookies():
    steam_id = request.cookies.get("steam_id")
    discord_id = request.cookies.get("discord_id")
    discord_username = request.cookies.get("discord_username")
    session = request.cookies.get("session")

    return (steam_id, discord_id, discord_username, session)

def delete_cookies(resp):
    resp.delete_cookie("discord_id")
    resp.delete_cookie("discord_username")
    resp.delete_cookie("steam_id")

async def add_user_and_render(mongo):

    steam_id, discord_id, discord_username, session = get_cookies()

    resp = make_response(render_template(
        "views/link.html", unlink_url="/unlink", discord_id=discord_id, steam_id=steam_id))
    delete_cookies(resp)

    tmp_session = hashlib.md5(str(str(steam_id)+str(discord_id)+str(
        datetime.now().strftime('%Y-%m-%d %H:%M'))).encode("UTF-8")).hexdigest()
    resp.set_cookie("session", tmp_session)

    if db_website.add_link_to_db(mongo, tmp_session, discord_id, steam_id, discord_username):
        await webhook.new_user_added(discord_id, discord_username, steam_id, )

    return resp

def get_discord_id(mongo):
    code = request.args.get("code")
    if code:
        token = discord_oauth.get_access_token(code)["access_token"]
        user = discord_oauth.get_user(token)

        session = db_website.fetch_session_by_discord_id(mongo, user["id"])
        link = db_website.fetch_ids_by_session(mongo, session)
        if link != False:
            resp = make_response(redirect("/link"))
            resp.set_cookie("steam_id", value=link["steam_id"])
            resp.set_cookie("discord_id", value=link["discord_id"])
            resp.set_cookie("session", value=link["session"])
            return resp

        resp = make_response(redirect("/link"))
        resp.set_cookie("discord_id", value=user["id"])
        resp.set_cookie("discord_username", value=user["username"])

        return resp
    else:
        return redirect("/link")

def get_steam_id(mongo):
    user = request.args.get("openid.identity")
    if user:
        parts = user.split("/")
        id = parts[len(parts) - 1]

        session = db_website.fetch_session_by_steam_id(mongo, id)
        link = db_website.fetch_ids_by_session(mongo, session)
        if link != False:
            resp = make_response(redirect("/link"))
            resp.set_cookie("steam_id", value=link["steam_id"])
            resp.set_cookie("discord_id", value=link["discord_id"])
            resp.set_cookie("session", value=link["session"])
            return resp

        resp = make_response(redirect("/link"))
        resp.set_cookie("steam_id", value=id)

        return resp
    else:
        return redirect("/link")