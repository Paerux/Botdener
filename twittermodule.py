import json

import tweepy
from discord.ext import commands  # noqa

from utilities import Utilities


class TwitterModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class TwitterStream(tweepy.StreamingClient):
        bot = None

        async def send_tweet(self, message):
            channel = self.bot.get_channel(891317992628031528)
            await channel.send(message)

        def assign_bot(self, bot):
            self.bot = bot

        def on_tweet(self, tweet):  # noqa
            print("on_tweet")

        def on_data(self, data):
            tweet = json.loads(data)
            if tweet['matching_rules'][0]['id'] == '1546126248472109057':
                name = 'Botdener'
            elif tweet['matching_rules'][0]['id'] == '1546126255929671680':
                name = 'Çöp Ark'
            else:
                name = 'Unknown'

            self.bot.loop.create_task(self.send_tweet(name + " tweeted:"))
            text = Utilities.case_sensitive_replace(tweet['data']['text'], 'lost ark', 'çöp ark')
            self.bot.loop.create_task(self.send_tweet(text))

        def on_errors(self, errors):
            print(errors)

        def on_connect(self):
            print("onconnect")

        def on_disconnect(self):
            print("ondisconnect")

        def on_exception(self, exception):
            print(exception)

        def on_request_error(self, code):
            print("request error")

