# import libs
import discord
from discord import guild, SlashCommandOptionType
from discord.ext import commands
from discord.commands import Option, permissions
from discord.ui import button, View
from discord.ext.commands import has_permissions
import logging
import json
import requests as req
from time import sleep
#import asyncio
logging.basicConfig(level=logging.INFO)

#setup vars
prefix = "sl:"
token = ""
sl_api_key = ""
sl_account_id = ""
server_id = [991854008438370324]

#read api data for sl and discord
with open("data.json", mode="r") as tokenFile:
    json_data = json.loads(tokenFile.read())
    token = json_data["discord_token"]
    sl_api_key = json_data["sl_api_key"]
    sl_account_id = json_data["sl_account_id"]
    tokenFile.close()
player_amount_url = f"https://api.scpslgame.com/serverinfo.php?id={sl_account_id}&key={sl_api_key}&players=true"

#setup client
client = commands.Bot(command_prefix=prefix, activity=discord.Game(name='with the scp sl api'))

@client.slash_command(guild_ids=server_id)
async def getplayers(ctx):
    "get the amount of people playing in the server"
    response = req.get(player_amount_url)
    json_data = response.json()
    if not json_data["Success"]:
        if response.status_code != 429:
            await ctx.send_response(f"there was an error trying to get the player amount in the server: ```{response}```")
        else:
            await ctx.send_response("slow down a bit! the scp sl servers have a rate limit so the bot can't get the player amount every 3 seconds.")
    else:
        players = json_data["Servers"]
        await ctx.send_response(f"```{players}```\n```{response}``` (should be <Response [200]>)")

client.run(token)
print("bot shutdown")