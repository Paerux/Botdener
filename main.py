import datetime
from discord.ext import commands  # noqa
import discord  # noqa
import yaml
from discord import FFmpegPCMAudio, ClientException  # noqa
import database
import Logger
from textmodule import TextModule
from utilities import Utilities
from voicemodule import VoiceRecognition
from twittermodule import TwitterModule

logmanager = Logger.LogManager()
logmanager.initialize()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


def load_config():
    with open('bot_config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


config = load_config()
bot.add_cog(VoiceRecognition(bot, config))
bot.add_cog(Utilities(bot))
bot.add_cog(TwitterModule(bot))
bot.add_cog(TextModule(bot, config))


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    twitter = TwitterModule.TwitterStream(config['twitter']['bearer_token'], wait_on_rate_limit=True)
    twitter.assign_bot(bot)
    twitter.filter(threaded=True)


bot.run(config['token'])
