import discord 
from discord.ext import commands, tasks
from random import choice

from music import music_cog

# your bot's command prefix and status
client = commands.Bot(command_prefix='#', activity = discord.Game(name="discord.gg | #help")) 
client.remove_command('help')
client.add_cog(music_cog(client))

#start-up
@client.event
async def on_ready(): 
    print("Logged in as {0.user}".format(client))

TOKEN = # your bot's token
client.run(TOKEN)