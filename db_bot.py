def fetch_link_by_session(mongo, session):
    link = mongo.links.find_one({})
    return

def fetch_link_by_discord_id(mongo, discord_id):
    link = mongo.links.find_one({"discord_id": str(discord_id)})
    if link:
        return link
    else:
        False

def fetch_link_by_steam_id(mongo, steam_id):
    link = mongo.links.find_one({"steam_id": str(steam_id)})
    if link:
        return link
    else:
        False