from datetime import datetime
import hashlib


def add_link_to_db(mongo, session, discord_id, steam_id, discord_username):
    db_link = mongo.db.links
    link = db_link.find_one({"discord_id": discord_id})

    if link: 
        return False
    else:
        new_link = {"discord_id": discord_id, "steam_id": steam_id, "discord_username": discord_username, "session": session}
        db_link.insert(new_link)
    return True

def remove_link_from_db(mongo, discord_id, steam_id):
    db_link = mongo.db.links
    
    if db_link.find_one({"discord_id": discord_id, "steam_id": steam_id}):
        db_link.delete_one({"discord_id": discord_id, "steam_id": steam_id})
        return True
    else:
        False

def fetch_session(mongo, discord_id):
        db_link = mongo.db.links
        link = db_link.find_one({"discord_id": discord_id})

        if link:
            tmp_session = hashlib.md5(str(str(steam_id)+str(discord_id)+str(datetime.now().strftime('%Y-%m-%d %H:%M'))).encode("UTF-8")).hexdigest()
            db_link.update({"discord_id": discord_id}, {"$set": {"session": tmp_session}})

            return tmp_session
        else:
            return False
