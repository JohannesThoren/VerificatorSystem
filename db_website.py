

from datetime import datetime
import hashlib

from os import link



def add_link_to_db(mongo, session, discord_id, steam_id, discord_username):
    db_link = mongo.db.links
    link = db_link.find_one({"discord_id": discord_id})

    if link:
        return False
    else:
        new_link = {"discord_id": discord_id, "steam_id": steam_id, "discord_username": discord_username,
                    "session": session, "togg_1": True, "togg_2": True, "togg_3": True, "togg_4": True}
        db_link.insert(new_link)
    return True


def remove_link_from_db(mongo, discord_id, steam_id):
    db_link = mongo.db.links

    if db_link.find_one({"discord_id": discord_id, "steam_id": steam_id}):
        db_link.delete_one({"discord_id": discord_id, "steam_id": steam_id})
        return True
    else:
        False


def fetch_link_by_session(mongo, session):
    db_link = mongo.db.links
    link = db_link.find_one({"session": session})
    if link:
        return link
    else:
        return False


def fetch_session_by_discord_id(mongo, discord_id):
    db_link = mongo.db.links
    link = db_link.find_one({"discord_id": discord_id})

    if link:
        tmp_session = hashlib.md5(str(str(
            discord_id)+str(datetime.now().strftime('%Y-%m-%d %H:%M'))).encode("UTF-8")).hexdigest()
        db_link.update({"discord_id": discord_id}, {
                       "$set": {"session": tmp_session}})

        return tmp_session
    else:
        return False


def fetch_session_by_steam_id(mongo, steam_id):
    db_link = mongo.db.links
    link = db_link.find_one({"steam_id": steam_id})

    if link:
        tmp_session = hashlib.md5(str(str(
            steam_id)+str(datetime.now().strftime('%Y-%m-%d %H:%M'))).encode("UTF-8")).hexdigest()
        db_link.update({"steam_id": steam_id}, {
                       "$set": {"session": tmp_session}})

        return tmp_session
    else:
        return False


def toggle(mongo, session, toggle):

    db_link = mongo.db.links
    link = db_link.find_one({"session": session})
    if link:
        state = link[f"togg_{toggle}"]
        if state == True:
            db_link.update({"session": session}, {
                           "$set": {f"togg_{toggle}": False}})
        elif state == False:
            db_link.update({"session": session}, {
                           "$set": {f"togg_{toggle}": True}})

    else:
        return False


def fetch_toggles(mongo, session):

    db_link = mongo.db.links
    link = db_link.find_one({"session": session})
    if link:
        if "togg_1" in link.keys():
            return (link["togg_1"], link["togg_2"], link["togg_3"], link["togg_4"])
        else:
            db_link.update({"session": session}, {
                           "$set": {"togg_1": True, "togg_2": True, "togg_3": True, "togg_4": True}})
            return fetch_toggles(mongo, session)
    else:
        return False
