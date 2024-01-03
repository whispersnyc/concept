from config import TOKEN, CHANNELS, LAZY_LOADING, CACHE
import discord
from hyperlink import Hyperlink, extractor
from asyncio import sleep
from concept import Concept

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
concepts, source_ids = {}, []
queue = None


def refresh(id): print("Refresh", "index" if id == -1 else id)
    

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


async def process_messages(concept=None, thread=None, id=None):
    """Process hyperlinks in text channel"""
    if not concept: concept = concepts[id]
    if not thread: thread = client.get_channel(id)

    concept.sites, concept.media = [], []
    async for msg in thread.history(limit=None):
        for url in extractor(msg.content):
            sort_link(concept, Hyperlink(url))
        for fl in msg.attachments:
            sort_link(concept, Hyperlink(fl.url,
                fl.filename, fl.content_type, msg.id))
    concept.export(CACHE)


async def process_all_channels(lazy_load=LAZY_LOADING):
    """Processes all channels and sorts their links."""
    for channel_id in CHANNELS:
        channel = client.get_channel(channel_id)
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        for thread in channel.threads:
            if CACHE and (cached := Concept.cached(thread.id)):
                concepts[thread.id] = cached
                continue
            from_forum = isinstance(channel, discord.ForumChannel)
            concept = concepts[thread.id] = (
                await create_concept(thread, from_forum))
            if concept.source:
                source_ids.append(concept.source)
            if not lazy_load:
                await process_messages(concept, thread)
            concept.export(CACHE)
    
    print("Done processing all channels.")


async def check_queue():
    while True:
        while not queue.empty():
            message, data = queue.get()
            print(message, data)
            if message == "refresh_concept":
                concept_id = int(data)
                if concept_id == -1:
                    await process_all_channels(False)
                else:
                    await process_messages(id=concept_id)
                if LAZY_LOADING: refresh(concept_id)
        await sleep(1)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(check_queue())
    await process_all_channels()
    refresh(-1)


def run_bot(message_queue):
    global queue
    queue = message_queue
    client.run(TOKEN)