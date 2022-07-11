import requests
from bs4 import BeautifulSoup
from discord.ext import commands  # noqa
import threading
import re
import lxml

import database
import utilities


class RSSModule(commands.Cog):
    def __init__(self, bot, interval):
        self.bot = bot
        self.interval = interval
        self.is_running = False
        self._timer = None

    def _run(self):
        self.is_running = False
        self.start()
        self.check_all_rss()

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def check_all_rss(self):
        self.check_rss('https://devtrackers.gg/warcraft.rss', 'DevTracker - WoW')
        self.check_rss('https://devtrackers.gg/lost-ark.rss', 'DevTracker - Çöp Ark')

    def check_rss(self, url, title):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        soup = BeautifulSoup(r.text, 'lxml')  # python console gives error on first one, works on second one??
        items = soup.findAll('item')
        item_dict = [
            {'title': a.find('title').text,
             'description': a.find('description').text,
             'guid': a.find('guid').text} for a in items]

        seen_guids = database.get_rss_list()

        for item in item_dict:
            if not item['guid'] in seen_guids:
                database.add_rss_id(item['guid'])
                print('Found new rss')
                cleartag = re.compile('<.*?>')
                self.bot.loop.create_task(self.send_status_message(title))
                message = re.sub(cleartag, '', item['description'])
                message = utilities.Utilities.case_sensitive_replace(message, 'lost ark', 'çöp ark')
                self.bot.loop.create_task(self.send_status_message(message))

    async def send_status_message(self, message):  # noqa
        channel = self.bot.get_channel(891317992628031528)
        await channel.send(message)
