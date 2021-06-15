import discord
from discord.ext import commands, tasks
from music import music_cog

# your bot's command pefix and status
client = commands.Bot(command_prefix='-', activity = discord.Game(name="discord.gg | -help")) 

client.remove_command('help')
client.add_cog(music_cog(client))

# start-up and login message
@client.event
async def on_ready(): 
    print("Logged in as {0.user}".format(client))

TOKEN = # your token id here
client.run(TOKEN)