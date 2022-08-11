# noinspection PyPackageRequirements
import discord
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)
bot = discord.Bot(debug_guilds=[1005477540456058901])


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online")


@bot.slash_command(name="hello", description="say hello to bot")
async def hello(ctx):
    await ctx.respond("hey")

bot.load_extension("music")
bot.run(os.getenv('TOKEN'))
