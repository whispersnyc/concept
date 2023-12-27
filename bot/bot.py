from bot.concept import Concept
from config import *
import discord
from os.path import exists, join
from urlextract import URLExtract

extractor = URLExtract()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

concepts, sources = {}, []


def add(dict, key, value): dict.setdefault(key, []).append(value)
def process_msg(concept, msg):
    for url in extractor.find_urls(msg.content) + msg.attachments:
        if isinstance(url, discord.Attachment): url = url.url
        if any([e in url for e in (".png", ".jpg", ".gif", ".mp4", ".mp3", ".ogg")]):
            add(concept.media, msg.id, url)
        else:
            add(concept.links, msg.id, url)


async def process_channels():
    for channel_id in CHANNELS:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        for thread in channel.threads:
            forum = isinstance(channel, discord.ForumChannel)
            concept = concepts[thread.id] = \
                await Concept.create(thread, forum)
            if concept.source: sources.append(concept.source)

            async for msg in thread.history(limit=None):
                process_msg(concept, msg)

    # second pass for post-thread connection
    for concept in concepts:
        if EXPORT and exists(EXPORT) and concept not in sources:
            fn = f"{EXPORT}/{concept.id}.md"
            with open(fn, "w", encoding='utf-8') as fl:
                if concept.post: fl.write(str(concept))


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await process_channels()
    print("Done processing")


def run_bot(): client.run(TOKEN)