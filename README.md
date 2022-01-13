# verificator
Verificator is a Discord and Steam linker and verifiaction bot and website. It has a Discord bot for handling discord roles and uses a webhook for sending updates. Verificator saves Steam and Discord ids of people using it.

*origianly made for willjum discord community.*

## Usecases
sy that you for example own a Rust or CSGO comunity server and someone does bad stuff in the discord channle, things that are banable, if this person is "verified" or "linked" then you can fetch their Steam id and ban them on the game server.

## Setup
the setup is very simple, there are alot of steps but they are streight forward.

### pre install
1. setup a discord channle with a webhook
2. setup a mongodb database

### install
1. git clone the repo or download it
2. open the folder you donwloaded
3. run `pip install -r requierments.txt` to install all dependencies
4. open the `env.json` file and fill out all your information

to start the system you just need to run the `webserver.py` and `bot.py` scripts. and if the `env.json` is correct, the system should be up and running

**Note: install instructions can be wrong if there are updates that changes things, updating instructions when i have time**

### branding
it is recommended to edit the `branding.json` file if not you will get errors but the site will still work.
