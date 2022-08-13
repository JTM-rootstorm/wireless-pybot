import asyncio
from concurrent.futures import Future

import discord
from discord import VoiceClient
from discord.ext import commands
from typing import Dict

import download_handler
import youtubedl
from media_info import MediaInfo


class Music(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        self.voice_client_dict: Dict[int, VoiceClient] = {}
        self.guild_video_queues: Dict[int, list] = {}

    def play_music_ffmpeg(self, ctx: discord.ApplicationContext, vc: VoiceClient, guild_id: int):
        guild_queue = self.guild_video_queues[guild_id]

        if guild_queue:
            future: Future[MediaInfo] = guild_queue.pop(0)
            media = future.result()

            if guild_queue:
                new_media = guild_queue[0]
                guild_queue[0] = download_handler.queue_video_for_download(new_media)

            asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing {media.videoTitle}"), self.bot.loop)
            vc.play(
                discord.FFmpegPCMAudio(
                    executable="ffmpeg.exe",
                    source=media.mediaPath
                ),
                after=lambda e: self.play_next(vc)
            )
        else:
            asyncio.sleep(90)
            if not vc.is_playing():
                asyncio.run_coroutine_threadsafe(vc.disconnect(), self.bot.loop)
                asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue"), self.bot.loop)

    def play_next(self, vc: VoiceClient):
        pass

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

            self.play_music_ffmpeg(ctx, voice_client, file_path)

            await ctx.respond(f"Connected to {voice_channel.name}, playing {video_title}")
        else:
            await ctx.respond("you need to be in a voice channel to do this")

    @commands.slash_command(name="playlist", description="figure out yt playlits")
    async def playlist(self, ctx: discord.ApplicationContext, url: str):
        await ctx.respond("Processing video(s)...")
        guild_id = ctx.author.guild.id
        guild_queue = self.guild_video_queues[guild_id]

        if guild_queue:
            guild_queue.append(youtubedl.process_playlist(url))
        else:
            guild_queue.append(youtubedl.process_playlist(url))
            med_info = guild_queue[0]
            guild_queue[0] = download_handler.queue_video_for_download(med_info)

        voice_channel = ctx.author.voice.channel
        voice_client = self.voice_client_dict.get(guild_id)

        if voice_channel is not None:
            if voice_client is None:
                self.voice_client_dict[guild_id] = voice_client = await voice_channel.connect()
            else:
                if not voice_client.is_playing():
                    if voice_client.channel is not voice_channel:
                        await voice_client.move_to(voice_channel)
                        self.play_music_ffmpeg(ctx, voice_client, guild_id)


def setup(bot):
    bot.add_cog(Music(bot))
