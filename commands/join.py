import discord
from discord.ext import commands


class Join(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    @commands.slash_command(name="join", description="fuck")
    async def join(self, ctx: discord.ApplicationContext):
        voice = ctx.author.voice

        if voice is not None:
            await voice.channel.connect()
            await ctx.respond(f"Connected and bound to {voice.channel.mention}!")
        else:
            await ctx.respond(
                "you need to be in a voice channel to use this"
            )

    @commands.slash_command(name="leave", description="leave the chat")
    async def leave(self, ctx: discord.ApplicationContext):
        voice = ctx.voice_client
        if voice is not None:
            await voice.disconnect(force=False)
            await ctx.respond(f"Left the VC")
        else:
            await ctx.respond("I'm not even in a channel")

    @commands.slash_command(name="play", description="play music")
    async def play(self, ctx: discord.ApplicationContext):
        voice_channel = ctx.author.voice.channel
        if voice_channel is not None:
            vc = await voice_channel.connect()
            vc.play(
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
