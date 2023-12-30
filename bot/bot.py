from concept import Concept
from config import *
import discord
from os.path import exists, join
from hyperlink import Hyperlink, extractor


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

concepts, source_ids = {}, []
    

async def create_concept(thread, from_forum):
    """Initialize Concept from Discord thread"""
    concept = Concept(thread.id, thread.name, thread.parent.name,
                      thread.parent.category.name)

    if from_forum: # fetch and set post/source
        concept.post = (await thread.fetch_message(thread.id)).content
        try: # find/remove <#...> in post (text channel id)
            if (txt := concept.post.strip()).startswith('<#'):
                source, txt = txt[2:].split('>', 1)
                source, concept.post = int(source), txt.strip()
                concept.source = source
        except Exception as e: print(thread.name, e)
    
    return concept


def sort_link(concept, link):
    if link.type.startswith(("image/", "video/")):
        concept.media.append(link)
    else:
        concept.sites.append(link)


async def process_channels():
    """Processes all channels and sorts their links."""
    for channel_id in CHANNELS:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        for thread in channel.threads:
            # Initialize Concept
            forum = isinstance(channel, discord.ForumChannel)
            concept = concepts[thread.id] = (
                await create_concept(thread, forum))
            if concept.source:
                source_ids.append(concept.source)

            # Process hyperlinks in text channel
            async for msg in thread.history(limit=None):
                for url in extractor(msg.content):
                    sort_link(concept, Hyperlink(url))
                for fl in msg.attachments:
                    sort_link(concept,
                              Hyperlink(fl.url, fl.filename, fl.content_type))

            # Export to file
            if EXPORT and exists(EXPORT):
                fn = join(EXPORT, str(thread.id) + ".md")
                with open(fn, "w", encoding='utf-8') as fl:
                    fl.write(str(concept))
    print("Done processing all channels.")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await process_channels()


def run_bot(): client.run(TOKEN)