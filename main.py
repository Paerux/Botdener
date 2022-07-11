import datetime
from discord.ext import commands  # noqa
import discord  # noqa
import yaml
from discord import FFmpegPCMAudio, ClientException  # noqa
import database
import Logger
from rssmodule import RSSModule
from serverstatusmodule import ServerStatusModule
from textmodule import TextModule
from utilities import Utilities
from voicemodule import VoiceModule
from twittermodule import TwitterModule

logmanager = Logger.LogManager()
logmanager.initialize()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


def load_config():
    with open('bot_config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


config = load_config()
bot.add_cog(VoiceModule(bot, config))
bot.add_cog(Utilities(bot))
bot.add_cog(TwitterModule(bot))
bot.add_cog(TextModule(bot, config))

serverstatusmodule = ServerStatusModule(bot, 10)
rssmodule = RSSModule(bot, 10)

bot.add_cog(rssmodule)
bot.add_cog(serverstatusmodule)


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    twitter = TwitterModule.TwitterStream(config['twitter']['bearer_token'], wait_on_rate_limit=True)
    print(twitter.get_rules())
    twitter.assign_bot(bot)
    twitter.filter(threaded=True)
    serverstatusmodule.start()
    rssmodule.start()


bot.run(config['token'])
