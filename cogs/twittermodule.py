import json
import logging

import tweepy
from discord.ext import commands  # noqa
from cogs.utilities import Utilities


class TwitterModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class TwitterStream(tweepy.StreamingClient):
        bot = None
        logger = logging.getLogger(__name__)

        async def send_tweet(self, message):
            channel = self.bot.get_channel(891317992628031528)
            await channel.send(message)

        def assign_bot(self, bot):
            self.bot = bot

        def on_tweet(self, tweet):  # noqa
            self.logger.info('on_tweet')

        def on_data(self, data):
            tweet = json.loads(data)
            self.logger.info(tweet)
            if tweet['matching_rules'][0]['id'] == '1546402585137004544':
                name = 'Botdener'
            elif tweet['matching_rules'][0]['id'] == '1546402592909139969':
                name = 'Çöp Ark'
            else:
                name = 'Unknown'

            self.bot.loop.create_task(self.send_tweet(name + " tweeted:"))
            text = Utilities.case_sensitive_replace(tweet['data']['text'], 'lost ark', 'çöp ark')
            self.bot.loop.create_task(self.send_tweet(text))

        def on_errors(self, errors):
            self.logger.error(errors)

        def on_connect(self):
            self.logger.info('on_connect')

        def on_disconnect(self):
            self.logger.info('on_disconnect')

        def on_exception(self, exception):
            self.logger.error(exception)

        def on_request_error(self, code):
            self.logger.error('on_request_error: ' + code)
