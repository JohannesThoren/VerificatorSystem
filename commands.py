import json
env = json.load(open("env.json"))

async def check_if_msg_is_command(msg):

    words = msg.content.split()
    bot_id = env["bot"]["id"]
    if len(words) != 0:
        if words[0] == f"<@!{bot_id}>" or words[0] == f"<@{bot_id}>":
            if words[1] == "steamid":
                return
            if words[1] == "discordid":
                return

                
    elif msg.author.name == "verificator-hook":
        user = ""
        embeds = msg.embeds
        for embed in embeds:
            dict = embed.to_dict()
            user_id = dict["fields"][0]["value"]




        await msg.add_reaction("✅")