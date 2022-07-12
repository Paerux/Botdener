import datetime
import logging
import os
import typing

from discord.ext import commands  # noqa
import random

import Logger
from cogs.utilities import Utilities

logger = logging.getLogger(__name__)


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

    @commands.command()
    async def erdener(self, ctx, todo: typing.Optional[str] = 'random'):
        voice = ctx.author.voice
        if not voice:
            logger.info("!erdener triggered but not in voice channel")
            return

        if todo == 'uyan':
            await Utilities.play_sound(voice.channel, 'sounds/erdener/uyanmis.mp3')
        elif todo == 'çöp':
            await Utilities.play_sound(voice.channel, 'sounds/erdener/copgame.mp3')
        elif todo is None or todo == '' or todo == 'random':
            await Utilities.play_sound(voice.channel, 'sounds/erdener/' + random.choice(os.listdir('sounds/erdener')))
        else:
            await ctx.channel.send('Unknown command')

    @commands.command()
    async def tulca(self, ctx, todo: typing.Optional[str] = 'random'):
        voice = ctx.author.voice
        if not voice:
            logger.info("!erdener triggered but not in voice channel")
            return

        if todo == 'lailai':
            await Utilities.play_sound(voice.channel, 'sounds/tulca/lailai.mp3')
        elif todo == 'brk':
            await Utilities.play_sound(voice.channel, 'sounds/tulca/brk.mp3')
        elif todo is None or todo == '' or todo == 'random':
            await Utilities.play_sound(voice.channel, 'sounds/tulca/' + random.choice(os.listdir('sounds/tulca')))
        else:
            await ctx.channel.send('Unknown command')

    @commands.command()
    async def ses(self, ctx, todo: typing.Optional[str] = 'random'):
        voice = ctx.author.voice
        if not voice:
            logger.info("!erdener triggered but not in voice channel")
            return

        if todo == 'alohade':
            await Utilities.play_sound(voice.channel, 'sounds/alohade.mp3')
        elif todo == 'rhino':
            await Utilities.play_sound(voice.channel, 'sounds/rhino.mp3')
        elif todo == 'dojo':
            await Utilities.play_sound(voice.channel, 'sounds/loa/dojo.mpeg')
        elif todo == 'öldüdeme':
            await Utilities.play_sound(voice.channel, 'sounds/oldulanisteoldu.mp3')
        elif todo == 'mantı':
            await Utilities.play_sound(voice.channel, 'sounds/manti.mp3')
        elif todo == 'tabi':
            await Utilities.play_sound(voice.channel, 'sounds/tabiefendim.mp3')
        elif todo == 'bruh':
            await Utilities.play_sound(voice.channel, 'sounds/bruh.mp3')
        elif todo == 'kırkharamiler':
            if ctx.author.id == 241562701497761792:
                await Utilities.play_sound(voice.channel, 'sounds/kirkharamiler.mp3')
            else:
                await ctx.channel.send('Tulca only command')
        else:
            await ctx.channel.send('Unknown command')

    @commands.command()
    async def hearthstone(self, ctx, todo: typing.Optional[str] = 'random'):
        voice = ctx.author.voice
        if not voice:
            logger.info("!erdener triggered but not in voice channel")
            return

        if todo == 'tirion':
            await Utilities.play_sound(voice.channel, 'sounds/hearthstone/tirion.mp3')
        elif todo is None or todo == '' or todo == 'random':
            await Utilities.play_sound(voice.channel, 'sounds/hearthstone/' + random.choice(os.listdir('sounds/hearthstone')))
        else:
            await ctx.channel.send('Unknown command')

    @commands.command()
    async def bag(self, ctx, todo: typing.Optional[str] = 'random'):
        voice = ctx.author.voice
        if not voice:
            logger.info("!erdener triggered but not in voice channel")
            return

        if os.path.exists('sounds/dota/bag/' + todo + '.mpeg'):
            await Utilities.play_sound(voice.channel, 'sounds/dota/bag/' + todo + '.mpeg')
        elif todo is None or todo == '' or todo == 'random':
            await Utilities.play_sound(voice.channel, 'sounds/dota/bag/' + random.choice(os.listdir('sounds/dota/bag')))
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
