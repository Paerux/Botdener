import datetime
import logging

import discord  # noqa
from discord import ClientException, FFmpegPCMAudio  # noqa
from discord.commands import ApplicationContext, Option  # noqa
from discord.ext import commands  # noqa
import speech_recognition as sr

import database
from cogs.utilities import Utilities


class VoiceModule(commands.Cog):

    def __init__(self, bot, config):
        self.bot = bot
        self.connections = {}
        self.config = config
        self.uyanmis_list = config['uyanmis_users']
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not before.channel and after.channel:
            self.logger.info(f'{member} has joined a voice channel')
            voice_channel = member.voice.channel
            if not voice_channel:
                return

            if member.id in self.uyanmis_list:
                last_uyanmis = database.get_last_uyanmis(str(member.id))
                if last_uyanmis is not None:
                    time_difference = (datetime.datetime.now() - last_uyanmis).seconds
                    if time_difference < 300:
                        return

                await Utilities.play_sound(voice_channel, 'sounds/erdener/uyanmis.mp3')
                database.add_uyanmis(str(member.id), datetime.datetime.now().strftime(database.DATE_FORMAT))

    @commands.command()
    async def kaybol(self, ctx):
        bot_connection: discord.VoiceClient = ctx.guild.voice_client
        if bot_connection:
            await bot_connection.disconnect()
        else:
            self.logger.warning('kaybol : Not connected to any channel')

    @commands.command()
    async def start(self, ctx):
        """
        Record your voice!
        """

        voice = ctx.author.voice

        if not voice:
            return await ctx.reply("You're not in a vc right now")

        try:
            vc = await voice.channel.connect()
            self.connections.update({ctx.guild.id: vc})
            sink = discord.sinks.MP3Sink()
            vc.start_recording(
                sink,
                self.finished_callback,
                ctx.channel,
            )
            await ctx.reply("The recording has started!")
        except ClientException as e:
            self.logger.error(e)

    @staticmethod
    async def finished_callback(sink, channel: discord.TextChannel, *args):
        recorded_users = [f" < @{user_id}>" for user_id, audio in sink.audio_data.items()]
        await sink.vc.disconnect()
        files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in
                 sink.audio_data.items()]

        # r = sr.Recognizer()
        #
        # audio_files = [i.file for i in sink.audio_data.values()]
        # for file in audio_files:
        #     with sr.AudioFile(file) as source:
        #         audio = r.record(source)
        #     try:
        #         # for testing purposes, we're just using the default API key
        #         # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        #         # instead of `r.recognize_google(audio)`
        #         print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language="tr-TR"))
        #     except sr.UnknownValueError:
        #         print("Google Speech Recognition could not understand audio")
        #     except sr.RequestError as e:
        #         print("Could not request results from Google Speech Recognition service; {0}".format(e))

        await channel.send(f"Finished! Recorded audio for {', '.join(recorded_users)}.", files=files)

    @commands.command()
    async def stop(self, ctx):
        """
        Stop recording.
        """
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            vc.stop_recording()
            del self.connections[ctx.guild.id]
        else:
            await ctx.reply("Not recording in this guild.")
