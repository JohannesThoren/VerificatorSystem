import secrets

from bson.objectid import ObjectId


def fetch_link_by_discord_id(mongo, token, check_token, discord_id):
    db_links = mongo.db.links
    link = db_links.find_one({"discord_id": str(discord_id)})

    if token != check_token:
        return {"err": "invalid token"}

    if link:
        return {"link": {"discord_id": link["discord_id"], "steam_id": link["steam_id"]}}
    else:
        return {"err": "could not find any link"}


def fetch_link_by_steam_id(mongo, token, check_token, steam_id):
    db_links = mongo.db.links
    link = db_links.find_one({"steam_id": str(steam_id)})

    if token != check_token:
        return {"err": "invalid token"}
        
    if link:
        return {"link": {"discord_id": link["discord_id"], "steam_id": link["steam_id"]}}
    else:
        return {"err": "could not find any link"}
