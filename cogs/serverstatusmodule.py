import logging
from discord.ext import commands  # noqa
import threading
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ServerStatusModule(commands.Cog):
    def __init__(self, bot, interval):
        self.bot = bot
        self.interval = interval
        self.is_running = False
        self._timer = None
        self.last_status = 'Live'

    def _run(self):
        self.is_running = False
        self.start()
        self.check_maintenance()

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()

        self.is_running = False

    def check_maintenance(self):
        req = requests.get('https://www.playlostark.com/en-gb/support/server-status')
        source_code = req.text
        soup = BeautifulSoup(source_code, 'html.parser')
        items = soup.select('.ags-ServerStatus-content-responses-response-server:-soup-contains("Kadan")')
        for tag in items:
            if tag.find('div', attrs={
                'class': 'ags-ServerStatus-content-responses-response-server-status '
                         'ags-ServerStatus-content-responses-response-server-status--good'}):
                if self.last_status == 'Down':
                    self.last_status = 'Live'
                    self.bot.loop.create_task(self.send_status_message('Kadan server is up Poggers'))
            elif tag.find('div', attrs={
                'class': 'ags-ServerStatus-content-responses-response-server-status '
                         'ags-ServerStatus-content-responses-response-server-status--maintenance'}):
                if self.last_status == 'Live':
                    self.last_status = 'Down'
                    self.bot.loop.create_task(self.send_status_message('Kadan server is up Down Sadge'))
            else:
                logger.warning('maintenance server tag not found')
                if self.last_status == 'Live':
                    self.last_status = 'Down'
                    self.bot.loop.create_task(self.send_status_message('Kadan server is up Down Sadge'))

    async def send_status_message(self, message):
        channel = self.bot.get_channel(891317992628031528)
        await channel.send(message)
