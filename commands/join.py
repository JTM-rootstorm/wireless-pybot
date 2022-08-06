import discord
from discord import VoiceClient
from discord.ext import commands
from typing import Dict


class Join(commands.Cog):
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

    @commands.slash_command(name="play", description="play music")
    async def play(self, ctx: discord.ApplicationContext):
        voice_channel = ctx.author.voice.channel
        guild_id = ctx.author.guild.id
        voice_client = self.voice_client_dict.get(guild_id)

        if voice_channel is not None:
            if voice_client is None:
                self.voice_client_dict[guild_id] = await voice_channel.connect()
                voice_client = self.voice_client_dict.get(guild_id)
            else:
                if voice_client.channel is not voice_channel:
                    if voice_client.is_playing():
                        voice_client.stop()
                    await voice_client.move_to(voice_channel)

            voice_client.play(
                discord.FFmpegPCMAudio(
                    executable="ffmpeg.exe",
                    source=r"./media/test.mp3"
                )
            )
            await ctx.respond(f"Connected to {voice_channel.name}, playing audio")
        else:
            await ctx.respond("you need to be in a voice channel to do this")


def setup(bot):
    bot.add_cog(Join(bot))
