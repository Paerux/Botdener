import discord  # noqa
from discord.commands import ApplicationContext, Option  # noqa
from discord.ext import commands  # noqa


class VoiceRecognition(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.connections = {}

    @commands.command()
    async def start(self, ctx):
        """
        Record your voice!
        """

        voice = ctx.author.voice

        if not voice:
            return await ctx.reply("You're not in a vc right now")

        vc = await voice.channel.connect()
        self.connections.update({ctx.guild.id: vc})

        sink = discord.sinks.WaveSink()

        vc.start_recording(
            sink,
            self.finished_callback,
            ctx.channel,
        )

        await ctx.reply("The recording has started!")

    @staticmethod
    async def finished_callback(sink, channel: discord.TextChannel, *args):
        recorded_users = [f" < @{user_id}>" for user_id, audio in sink.audio_data.items()]
        await sink.vc.disconnect()
        files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in
                 sink.audio_data.items()]
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
