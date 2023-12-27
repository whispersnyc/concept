from bot.concept import Concept
from config import *
from os.path import join
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

concepts, sources = {}, []


async def process_channels():
    for channel_id in CHANNELS:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        for thread in channel.threads:
            forum = isinstance(channel, discord.ForumChannel)
            concept = concepts[id := thread.id] = \
                await Concept.create(thread, forum)
            if concept.source: sources.append(concept.source)

            if EXPORT and True: # TODO: check path validity
                with open(f"{EXPORT}/{id}.md", "w", encoding='utf-8') as fl:
                    if post := concept.post: fl.write(post)
    
    # async for msg in thread.history(limit=None): pass
    


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await process_channels()
    print("Done processing")


def run_bot(): client.run(TOKEN)