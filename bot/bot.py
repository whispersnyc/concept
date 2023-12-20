from config import *
import discord
from discord.ext import commands

intents = discord.Intents.default()

class Bot(commands.Bot):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if str(message.channel.id) in CHANNELS:
            print(f'Message from {message.author}: {message.content}')

bot = Bot(command_prefix='!', intents=intents)
bot.run(TOKEN)