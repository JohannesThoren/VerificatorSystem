from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

import json
import requests
import discord_oauth

from werkzeug.wrappers import response
app = Flask(__name__, static_folder='static')
env = json.load(open("env.json"))



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/discord')
def discord():
    code = request.args.get("code")
    if code:
        token = discord_oauth.get_access_token(code)["access_token"]
        user = discord_oauth.get_user(token)

        return user
    else:
        return render_template("views/discord.html", discord_url = env["oauth_discord"]["sign_in_url"])

@app.route('/link')
def link():
    

    return render_template('views/link.html', discord_url = env["oauth_discord"]["sign_in_url"])



if __name__ == "__main__":
    app.run(debug=True, host=env["webserver"]["host"], port=env["webserver"]["port"])