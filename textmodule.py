import datetime
from discord.ext import commands  # noqa
import random
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
            print('triggered')
            rand = random.randint(0, 100)
            if rand < 25 and (datetime.datetime.now() - self.last_reaction).seconds > 300:
                self.last_reaction = datetime.datetime.now()
                await message.add_reaction('<:ICANT:980378964692434975>')
            else:
                if (datetime.datetime.now() - self.last_reaction).seconds > 300:
                    self.last_reaction = datetime.datetime.now()
                    await message.channel.send(Utilities.case_sensitive_replace(message.content, 'lost ark', 'çöp ark'))

        await self.bot.process_commands(message)
