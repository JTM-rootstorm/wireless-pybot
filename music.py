import discord
from discord import VoiceClient
from discord.ext import commands
from typing import Dict
import youtubedl


class Music(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        self.isPlaying = False
        self.voice_client_dict: Dict[int, VoiceClient] = {}

    @commands.slash_command(name="leave", description="leave the chat")
    async def leave(self, ctx: discord.ApplicationContext):
        voice = self.voice_client_dict[ctx.author.guild.id]

        if voice is not None:
            if not ctx.author.voice.channel:
                await ctx.respond("You need to be in a VC to use this")
                return

            if ctx.author.voice.channel is not ctx.voice_client.channel:
                await ctx.respond("We're not even in the same channel")
                return

            del self.voice_client_dict[ctx.author.guild.id]
            await voice.disconnect(force=True)
            await ctx.respond(f"Left the VC")
        else:
            await ctx.respond("I'm not even in a channel")

    @commands.slash_command(name="play", description="play from a URL")
    async def play(self, ctx: discord.ApplicationContext, url: str):
        await ctx.respond(f"Grabbing video...")
        (video_title, video_duration, file_path) = youtubedl.get_video(url)

        voice_channel = ctx.author.voice.channel
        guild_id = ctx.author.guild.id
        voice_client = self.voice_client_dict.get(guild_id)

        if voice_channel is not None:
            if voice_client is None:
                self.voice_client_dict[guild_id] = voice_client = await voice_channel.connect()
            else:
                if voice_client.is_playing():
                    voice_client.stop()
                if voice_client.channel is not voice_channel:
                    await voice_client.move_to(voice_channel)

            voice_client.play(
                discord.FFmpegPCMAudio(
                    executable="ffmpeg.exe",
                    source=file_path
                )
            )
            await ctx.respond(f"Connected to {voice_channel.name}, playing {video_title}")
        else:
            await ctx.respond("you need to be in a voice channel to do this")


def setup(bot):
    bot.add_cog(Music(bot))
