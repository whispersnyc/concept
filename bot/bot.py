from bot.concept import Concept
from config import *
import discord
from os.path import exists, join
from bot.hyperlink import Hyperlink, extractor


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

concepts, source_ids = {}, []


def sort_link(concept, link):
    if link.type == "media":
        concept.media.append(link)
    else:
        concept.sites.append(link)


async def process_channels():
    for channel_id in CHANNELS:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        for thread in channel.threads:
            forum = isinstance(channel, discord.ForumChannel)
            concept = concepts[thread.id] = \
                await Concept.Discord_thread(thread, forum)
            if concept.source: source_ids.append(concept.source)

            async for msg in thread.history(limit=None):
                for url in extractor(msg.content):
                    sort_link(concept, Hyperlink(url))
                for fl in msg.attachments:
                    sort_link(concept,
                        Hyperlink(fl.url, fl.filename, fl.content_type))

            if EXPORT and exists(EXPORT):
                fn = f"{EXPORT}/{thread.id}.md"
                with open(fn, "w", encoding='utf-8') as fl:
                    fl.write(str(concept))


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await process_channels()
    print("Done processing")


def run_bot():
    client.run(TOKEN)