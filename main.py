import logging
import random
import re
from datetime import datetime
from discord.ext import commands # noqa

import discord  # noqa
import speech_recognition as sr
import yaml
from discord import FFmpegPCMAudio  # noqa
from enum import Enum

import database

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

voice_client = discord.VoiceClient
r = sr.Recognizer()

last_reaction = datetime.now()
last_copark = datetime.now()


def load_config():
    with open('bot_config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


config = load_config()
uyanmis_list = config['uyanmis_users']


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    with sr.AudioFile(config['sounds']['uyan']) as source:
        audio = r.record(source)
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language="tr-TR"))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global last_reaction
    global last_copark
    if "lost ark" in message.content.lower():
        rand = random.randint(0, 100)
        if rand < 50 and (datetime.now() - last_reaction).seconds > 300:
            last_reaction = datetime.now()
            await message.add_reaction('<:ICANT:980378964692434975>')
        else:
            rand = random.randint(0, 100)
            if rand < 50 and (datetime.now() - last_copark).seconds > 300:
                last_copark = datetime.now()
                await message.channel.send(case_sensitive_replace(message.content, 'lost ark', 'çöp ark'))


@client.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        print(f'{member} has joined a voice channel')
        voice_channel = member.voice.channel
        if not voice_channel:
            return

        if member.id in uyanmis_list:
            last_uyanmis = database.get_last_uyanmis(str(member.id))
            if last_uyanmis is not None:
                time_difference = (datetime.now() - last_uyanmis).seconds
                print(time_difference)
                if time_difference > 300:
                    await play_sound(member, voice_channel)
            else:
                await play_sound(member, voice_channel)


async def play_sound(member, voice_channel):
    database.add_uyanmis(str(member.id), datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    voice = await join_channel(voice_channel)
    source = FFmpegPCMAudio('sounds/uyanmis.mp3')
    voice.play(source)


async def join_channel(channel):
    bot_connection: discord.VoiceClient = channel.guild.voice_client
    if bot_connection:
        await bot_connection.move_to(channel)
        return bot_connection
    else:
        return await channel.connect()


def case_sensitive_replace(string, old, new):
    """ replace occurrences of old with new, within string
        replacements will match the case of the text it replaces
    """

    def repl(match):
        current = match.group()
        result = ''
        all_upper = True
        for i, c in enumerate(current):
            if i >= len(new):
                break
            if c.isupper():
                result += new[i].upper()
            else:
                result += new[i].lower()
                all_upper = False
        # append any remaining characters from new
        if all_upper:
            result += new[i + 1:].upper()
        else:
            result += new[i + 1:].lower()
        return result

    regex = re.compile(re.escape(old), re.I)
    return regex.sub(repl, string)


bot = commands.Bot('!')
connections = {}


class Sinks(Enum):
    mp3 = discord.sinks.MP3Sink()
    wav = discord.sinks.WaveSink()
    pcm = discord.sinks.PCMSink()
    ogg = discord.sinks.OGGSink()
    mka = discord.sinks.MKASink()
    mkv = discord.sinks.MKVSink()
    mp4 = discord.sinks.MP4Sink()
    m4a = discord.sinks.M4ASink()


async def finished_callback(sink, channel: discord.TextChannel, *args):
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    await sink.vc.disconnect()
    files = [
        discord.File(audio.file, f"{user_id}.{sink.encoding}")
        for user_id, audio in sink.audio_data.items()
    ]
    await channel.send(
        f"Finished! Recorded audio for {', '.join(recorded_users)}.", files=files
    )


@bot.command()
async def start(ctx: discord.ApplicationContext, sink: Sinks):
    """
    Record your voice!
    """
    voice = ctx.author.voice

    if not voice:
        return await ctx.respond("You're not in a vc right now")

    vc = await voice.channel.connect()
    connections.update({ctx.guild.id: vc})

    vc.start_recording(
        sink.value,
        finished_callback,
        ctx.channel,
    )

    await ctx.respond("The recording has started!")


@bot.command()
async def stop(ctx: discord.ApplicationContext):
    """Stop recording."""
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        del connections[ctx.guild.id]
        await ctx.delete()
    else:
        await ctx.respond("Not recording in this guild.")

client.run(config['token'])
