import discord
from discord.channel import VoiceChannel
from discord.ext import commands
import asyncio
from discord.ext import commands, tasks

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False
                
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play")
    async def p(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send(":x: You are **not** in any voice channel!")

        else:
            try:
                if not voice_channel.channel == self.vc.channel:
                    return
                
                else:
                    song = self.search_yt(query)
                    if type(song) == type(True):
                        await ctx.send(":x: **You almost broke me!**")

            except:
                if self.vc == "":
                    song = self.search_yt(query)
                    if type(song) == type(True):
                        await ctx.send(":x: **You almost broke me!**")

            try: 
                if voice_channel.channel == self.vc.channel:
                    if self.vc.is_playing():
                        await ctx.send(":white_check_mark: Enqueued **{}**! :thumbsup:".format(song['title']))
                    if not self.vc.is_playing():
                        await ctx.send(":white_check_mark: Now playing **{}**! :thumbsup:".format(song['title']))
                
                else:
                    await ctx.send(":x: You are **not** in my voice channel!")
            
            except:
                if self.vc == "":
                    await ctx.send(":white_check_mark: Now playing **{}**! :thumbsup:".format(song['title']))

            self.music_queue.append([song, ctx.author.voice.channel])
                    
            if self.is_playing == False:
                await self.play_music()

    @commands.command(name="queue")
    async def q(self, ctx):
       voice_channel = ctx.author.voice
       if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send(":x: You are **not** in any voice channel!")

       
       if voice_channel is None:
            return
       elif self.vc == "":
            await ctx.send(":x: I am **not** connected to a voice channel!")

       if self.vc == "":
            return 
       elif not self.vc.is_playing():
            await ctx.send(":x: I am **not** playing any songs!")

       if voice_channel.channel == self.vc.channel and self.vc.is_playing():
            retval = ""
            for i in range(0, len(self.music_queue)):
                retval += self.music_queue[i][0]['title'] + "\n"

            print(retval)
            if retval != "":
                await ctx.send(retval)
            else:
                await ctx.send(":x: **No music in queue**!")

    @commands.command(name="skip")
    async def skip(self, ctx):
        voice_channel = ctx.author.voice
        
        if voice_channel is None:
            await ctx.send(":x: You are **not** in a voice channel!")

        try:
            if voice_channel is None:
                return
            elif self.vc == "":
                await ctx.send(":x: I am **not** connected to a voice channel!")
        except:
            if self.vc == "":
                return 
            elif not self.vc.is_playing():
                await ctx.send(":x: I am **not** playing any songs!")

        if voice_channel.channel == self.vc.channel:
            if self.vc.is_playing():
                self.vc.stop()
                await ctx.send(":fast_forward: **Skipped** :thumbsup:")
            else:
                await ctx.send(":x: **No music playing**")

        else:
            await ctx.send(":x: You are **not** in my voice channel!")
    
    @commands.command(name="pause")
    async def pause(self, ctx):
        voice_channel = ctx.author.voice
        paused = False

        if voice_channel is None:
            await ctx.send(":x: You are **not** in a voice channel!")

        try:
            if voice_channel is None:
                return
            elif self.vc == "":
                await ctx.send(":x: I am **not** connected to a voice channel!")
        except:
            if self.vc == "":
                return 
            elif not self.vc.is_playing():
                await ctx.send(":x: I am **not** playing any songs!")
       
        if voice_channel.channel == self.vc.channel:
            if self.vc.is_paused():
                await ctx.send(":x: Song is **already paused**!")
                paused = True

            if self.is_playing == True and paused == False:
                self.vc.pause()
                await ctx.send(":white_check_mark: **Paused the song!** :thumbsup:")

            if not self.vc.is_paused() and not self.vc.is_playing():
                await ctx.send(":x: I am **not** playing any songs!")

        else:
            await ctx.send(":x: You are **not** in my voice channel!")

    @commands.command(name="resume")
    async def resume(self, ctx):
        voice_channel = ctx.author.voice
        resumed = False

        if voice_channel is None:
            await ctx.send(":x: You are **not** in a voice channel")

        if voice_channel is None:
            return

        elif self.vc == "":
            await ctx.send(":x: I am **not** connected to a voice channel!")
        
        if self.vc == "":
            return 

        elif not self.vc.is_playing():
            await ctx.send(":x: I am **not** playing any songs!")
       
        if voice_channel.channel == self.vc.channel:
            if not self.vc.is_paused() and self.vc.is_playing():
                await ctx.send(":x: **Song is not paused!**")
                resumed = True

            if self.is_playing == True and resumed == False:
                self.vc.resume()
                await ctx.send(":white_check_mark: **Resumed the song!** :thumbsup:")

        else:
            await ctx.send(":x: You are **not** in my voice channel!")

    @commands.command(name="leave")
    async def leave(self, ctx):
        voice_channel = ctx.author.voice

        if voice_channel is None:
            await ctx.send(":x: You are **not** in a voice channel")

        if voice_channel is None:
            return

        elif self.vc == "":
            await ctx.send(":x: I am **not** connected to a voice channel!")
        
        if self.vc == "":
             return 

        elif not self.vc.is_connected():
            await ctx.send(":x: I am **not** connected to a voice channel!")
       
        if voice_channel.channel == self.vc.channel:
                await self.vc.disconnect()
                self.vc = ""
                await ctx.send(":white_check_mark: **Sucessfully disconnected**")

        else:
            await ctx.send(":x: You are **not** in my voice channel!")

    @commands.command(name="help")
    async def help(message, ctx):
        embedVar = discord.Embed(title="List of commands", description="Helps you use the bot", color=0x808080)
        embedVar.add_field(name="-play", value="Plays a selected song from YouTube", inline=False)
        embedVar.add_field(name="-queue", value="Displays the current songs in queue", inline=False)
        embedVar.add_field(name="-skip", value="Skips the current song being played", inline = False)
        embedVar.add_field(name="-pause", value="Pause the song you are listening to now", inline = False)
        embedVar.add_field(name="-resume", value="Resume the song you had paused", inline = False)
        embedVar.add_field(name="-leave", value="Disconnect the bot from a voice channel", inline = False)
        await ctx.send(embed=embedVar)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if self.vc.is_connected() and len(self.vc.channel.members) == 1:
                await asyncio.sleep(30)
                await self.vc.disconnect()
                self.vc = ""
                CHANNEL_ID = 770946338795683871
                await client.get_channel(CHANNEL_ID).send(f"**{member.mention} disconnected and I'm lonely now!**")
        except:
            return

client = commands.Bot(command_prefix='-', activity = discord.Game(name="discord.gg | -help"))
client.remove_command('help')
client.add_cog(music_cog(client))

@client.event
async def on_ready(): #start-up
    print("Logged in as {0.user}".format(client))

TOKEN = "ODQ5MTg5NzY4ODA0OTU4MjA4.YLXjmg.a2k7hSie13qbpVk6AbaJmnxgJHU"
client.run(TOKEN)