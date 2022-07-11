import datetime

from discord import FFmpegPCMAudio, ClientException
from discord.ext import commands  # noqa
import random

import utilities
import voicemodule
from utilities import Utilities


class TextModule(commands.Cog):
    last_reaction = datetime.datetime.now() - datetime.timedelta(seconds=300)

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.uyanmis_list = self.config['uyanmis_users']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "lost ark" in message.content.lower():
            await self.react_lost_ark(message)

        await self.bot.process_commands(message)

    @commands.command()
    async def uyan(self, ctx):
        voice = ctx.author.voice
        if not voice:
            print("!uyan triggered but not in voice channel")
            return

        try:
            voice = await utilities.Utilities.join_channel(voice.channel)
            source = FFmpegPCMAudio('sounds/uyanmis.mp3')
            voice.play(source)
        except ClientException as exception:
            print(exception)

    async def react_lost_ark(self, message):
        print('triggered')
        rand = random.randint(0, 100)
        if rand < 25 and (datetime.datetime.now() - self.last_reaction).seconds > 300:
            self.last_reaction = datetime.datetime.now()
            await message.add_reaction('<:ICANT:980378964692434975>')
        else:
            if (datetime.datetime.now() - self.last_reaction).seconds > 300:
                self.last_reaction = datetime.datetime.now()
                await message.channel.send(Utilities.case_sensitive_replace(message.content, 'lost ark', 'çöp ark'))
