import random
from datetime import datetime
import discord
import logging
from discord import FFmpegPCMAudio
import database
import speech_recognition as sr
import re
import yaml

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

uyanmis_list = [217762767120105472, 169562873616531456, 124328951391846400, 172917614559887361, 129655277665386496,
                229030342277726208, 241825884535783424, 158132429570179072,
                213101741049249792, 160515892847968256,
                248299259202502666, 226501613173473280]

client = discord.Client()

voice_client = discord.VoiceClient
r = sr.Recognizer()

last_reaction = datetime.now()
last_copark = datetime.now()


def load_config():
    with open('bot_config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


config = load_config()


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

    if "lost ark" in message.content.lower():
        rand = random.randint(0, 100)
        if rand < 50 and (datetime.now() - last_reaction).seconds > 300:
            await message.add_reaction('<:ICANT:980378964692434975>')
        else:
            rand = random.randint(0, 100)
            if rand < 50 and (datetime.now() - last_copark).seconds > 300:
                await message.channel.send(case_sensitive_replace(message.content, 'lost ark', 'çöp ark'))

    if "!xd" in message.content:
        await play_sound(message.author, message.author.voice.channel)


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


client.run(config['bot_token'])
