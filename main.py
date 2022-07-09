import random
import datetime
from discord.ext import commands  # noqa
import discord  # noqa
import speech_recognition as sr
import yaml
from discord import FFmpegPCMAudio  # noqa
import database
import Logger
from utilities import Utilities
from voicerecognition import VoiceRecognition

logmanager = Logger.LogManager()
logmanager.initialize()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.add_cog(VoiceRecognition(bot))
bot.add_cog(Utilities(bot))
r = sr.Recognizer()

last_reaction = datetime.datetime.now() - datetime.timedelta(seconds=300)
last_copark = datetime.datetime.now() - datetime.timedelta(seconds=300)


def load_config():
    with open('bot_config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


config = load_config()
uyanmis_list = config['uyanmis_users']


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
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


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    global last_reaction
    global last_copark

    if "lost ark" in message.content.lower():
        print('triggered')
        rand = random.randint(0, 100)
        if rand < 50 and (datetime.datetime.now() - last_reaction).seconds > 300:
            last_reaction = datetime.datetime.now()
            await message.add_reaction('<:ICANT:980378964692434975>')
        else:
            rand = random.randint(0, 100)
            if rand < 50 and (datetime.datetime.now() - last_copark).seconds > 300:
                last_copark = datetime.datetime.now()
                await message.channel.send(Utilities.case_sensitive_replace(message.content, 'lost ark', 'çöp ark'))

    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        print(f'{member} has joined a voice channel')
        voice_channel = member.voice.channel
        if not voice_channel:
            return

        if member.id in uyanmis_list:
            last_uyanmis = database.get_last_uyanmis(str(member.id))
            if last_uyanmis is not None:
                time_difference = (datetime.datetime.now() - last_uyanmis).seconds
                print(time_difference)
                if time_difference > 300:
                    await play_sound(member, voice_channel)
            else:
                await play_sound(member, voice_channel)


async def play_sound(member, voice_channel):
    database.add_uyanmis(str(member.id), datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
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


bot.run(config['token'])
