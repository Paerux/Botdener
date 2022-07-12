import datetime
import logging
import os
import typing

from discord.ext import commands  # noqa
import random
from cogs.utilities import Utilities


class TextModule(commands.Cog):
    last_reaction = datetime.datetime.now() - datetime.timedelta(seconds=300)

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.uyanmis_list = self.config['uyanmis_users']
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "lost ark" in message.content.lower():
            await self.react_lost_ark(message)

    @commands.command()
    async def erdener(self, ctx, todo: typing.Optional[str] = 'random'):
        voice = ctx.author.voice
        if not voice:
            self.logger.info("!erdener triggered but not in voice channel")
            return

        if todo == 'uyan':
            await Utilities.play_sound(voice.channel, 'sounds/erdener/uyanmis.mp3')
        elif todo == 'çöp':
            await Utilities.play_sound(voice.channel, 'sounds/erdener/copgame.mp3')
        elif todo is None or todo == '' or todo == 'random':
            await Utilities.play_sound(voice.channel, 'sounds/erdener/' + random.choice(os.listdir('sounds/erdener')))
        else:
            await ctx.channel.send('Unknown command')

    async def react_lost_ark(self, message):
        rand = random.randint(0, 100)
        if (datetime.datetime.now() - self.last_reaction).seconds > 300:
            self.last_reaction = datetime.datetime.now()
            if rand < 25:
                await message.add_reaction('<:ICANT:980378964692434975>')
            else:
                await message.channel.send(Utilities.case_sensitive_replace(message.content, 'lost ark', 'çöp ark'))
