# discord.py 

### Commands

1. Play music command
2. Check list of queued songs command
3. Skip the song playing right now
4. Pause a song playing right now
5. Resume a song that has been paused
6. Leave a voice channel
7. Improved help command using embeds

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- 100% coverage of the supported Discord API.
- Optimised in both speed and memory.

Installing
----------

**Python 3.5.3 or higher is required**

To install the library without full voice support, you can just run the following command:

    # Linux/macOS
    python3 -m pip install -U discord.py

    # Windows
    py -3 -m pip install -U discord.py

Otherwise to get voice support you should run the following command:

    # Linux/macOS
    python3 -m pip install -U "discord.py[voice]"

    # Windows
    py -3 -m pip install -U discord.py[voice]


To install the development version, do the following:

    $ git clone https://github.com/jeffzy15/discord.py.git
    $ cd discord.py
    $ python3 -m pip install -U .[voice]
    
 
To install the other dependencies
 
 Check the [Requirements](https://github.com/jeffzy15/discord.py/blob/master/requirements.txt) document
 
 
To install ffmpeg (**very important**)
 
Visit [FFMPEG Website](https://www.ffmpeg.org/)
 
Optional Packages
-----------------

[PyNaCl](https://pypi.org/project/PyNaCl) for voice support

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)

### Error Handling

1. Ensure user is in a voice channel to connect the bot
2. Check that author of the command is in same voice channel as the bot to use it
3. Check that the command called is valid:

   Command: #skip
   
   ```python
   if self.vc.is_playing():
        self.vc.stop()
      
   else:
        await ctx.send("No music playing!")
   ```
         
   Check [music.py](https://github.com/jeffzy15/discord.py/blob/master/music.py) for more examples


Links
------

- [Documentation](https://discordpy.readthedocs.io/en/latest/index.html)
- [Official Discord Server](https://discord.gg/r3sSKJJ)
- [Discord API](https://discord.gg/discord-api)
