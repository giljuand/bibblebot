import discord
from discord.ext import commands, tasks
import random
import os
import asyncio

intents = discord.Intents.default()  # Adjust intents if you need more permissions
intents.message_content = True
intents.voice_states = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

#path to audio files
AUDIO_FOLDER = "Audio"
FFMPEG_OPTIONS = {'options': 'vn'} #FFmpeg options

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    play_random_audio.start() #start random audio playback task

async def play_audio_in_channel(channel, audio_file):
    """ connects to a voice channel, plays audio file, then disconnects."""
    try:
        #connect to voice channel"
        vc = await channel.connect()
        #play the audio file
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=audio_file),
                after=lambda e: print(f"finished playing: {audio_file}"))
        #wait for playback to finish
        while vc.is_playing():
            await asyncio.sleep(1)
        #disconnect after playback
        await vc.disconnect()
    except Exception as e:
        print(f"Error: {e}")

@tasks.loop(seconds=10) #check for active voice channels every 10 seconds
async def play_random_audio():
    """randomly joins active voice channel, plays audio file, and leaves"""
    for guild in bot.guilds:
        #find all active voice channels in the guild
        active_channels = [
            channel for channel in guild.voice_channels
            if len(channel.members) > 0 #channel must have at least one person
        ]
        if active_channels:
            #choose a random voice channel
            target_channel = random.choice(active_channels)
            #choose a random audio file from the folder
            audio_file = os.path.join(AUDIO_FOLDER, random.choice(os.listdir(AUDIO_FOLDER)))
            # play the audio in the chosen channel
            await play_audio_in_channel(target_channel, audio_file)
            #wait for a dandom interval (in seconds) before playing again
            await asyncio.sleep(random.randint(15, 30))
@bot.command()
async def bibble_stop(ctx):
    if ctx.author.id == 1309928794835910807:
        await ctx.send("alright goodbye :)")
        await bot.close()
    else:
        await ctx.send("NO bitch! >:) *pionts gun at u*")

bot.run("BOT TOKEN HERE")