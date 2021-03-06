import logging
import re

import discord
from discord import FFmpegPCMAudio, ClientException
from discord.ext import commands  # noqa


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def clear(self, ctx, number):
        messages = await ctx.channel.history(limit=int(number)).flatten()
        await ctx.channel.delete_messages(messages)

    @staticmethod
    def case_sensitive_replace(string, old, new):
        length_old = len(old.split())
        length_new = len(new.split())

        if length_old == length_new > 1:
            for x in range(length_new):
                string = Utilities.case_sensitive_replace(string, old.split()[x], new.split()[x])

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

    @staticmethod
    async def join_channel(channel):
        bot_connection: discord.VoiceClient = channel.guild.voice_client
        if bot_connection:
            await bot_connection.move_to(channel)
            return bot_connection
        else:
            return await channel.connect()

    @staticmethod
    async def play_sound(voice_channel, sound):
        try:
            voice = await Utilities.join_channel(voice_channel)
            source = FFmpegPCMAudio(sound)
            voice.play(source)
        except ClientException as e:
            logging.getLogger(__name__).error(e)
