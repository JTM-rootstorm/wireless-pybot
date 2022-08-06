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
            await ctx.send(f"Connected and bound to {voice.channel.mention}!")
        else:
            await ctx.send(
                "you need to be in a voice channel to use this"
            )

    @commands.slash_command(name="leave", description="leave the chat")
    async def leave(self, ctx: discord.ApplicationContext):
        voice = ctx.voice_client
        if voice is not None:
            await voice.disconnect(force=False)
            await ctx.send(f"Left the VC")
        else:
            await ctx.send("I'm not even in a channel")


def setup(bot):
    bot.add_cog(Join(bot))
