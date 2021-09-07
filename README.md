# Discord.py-Bot

Discord bot written in Python that does basic moderation tasks and has a few fun games.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

Set up a application in the [Discord Developer Portal](https://discord.com/developers/applications).

![alt text](https://i.imgur.com/yKzUBU2.png)

Make a new application and set up a bot for it.

![alt text](https://i.imgur.com/jflJYrY.png)

Make sure to select `SERVER MEMBERS INTENT` and `PRESENCE INTENT` under Privileged Gateway Intents, as it will not work without them.

Copy its token and paste it into `info.py` where it says `yourToken`

---

Run `main.py` with 
```bash
python3 main.py
```
It should give an output of the username of the bot and the cogs that were loaded.

---

## Adding to a server

Adding a bot to a server is easy!
Go to the OAuth2 tab in the sidebar and select `bot` in Scopes and `administrator` in Bot Permissions.

Then copy the OAuth2 URL which will look something like this:

[https://discord.com/api/oauth2/authorize?client_id=00000000000&permissions=8&scope=bot](https://discord.com/api/oauth2/authorize?client_id=00000000000&permissions=8&scope=bot)

And grant it access to your server, and your done!

---

Apologies for the poor commenting, I plan on fixing that soon, as this was one of my first major python projects.

## License
[MIT](https://choosealicense.com/licenses/mit/)
