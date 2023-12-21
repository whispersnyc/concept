from config import *  # TOKEN, CHANNELS
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def shorten(string, chars):
    return string[:min(len(string), chars)]

async def check_channels():
    for channel_id in CHANNELS:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        if isinstance(channel, discord.ForumChannel):
            for thread in channel.threads:
                print("post:", channel.category, channel.name, thread.name)
                async for message in thread.history(limit=1):
                    print('\t', shorten(message, 25))
        
        elif isinstance(channel, discord.TextChannel):
            for thread in channel.threads: # first pinned message in thread
                print("thread:", channel.category, channel.name, thread.name)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await check_channels()

client.run(TOKEN)