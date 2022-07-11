import asyncio
import re

import discord
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


