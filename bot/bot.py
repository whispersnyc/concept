from bot.concept import Concept
from bot.config import TOKEN, CHANNELS
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

concepts, sources = {}, []
cache = {} # read catch


async def check_channels():
    for channel_id in CHANNELS:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        for thread in channel.threads:
            concept, id = Concept(thread), thread.id
            if isinstance(channel, discord.ForumChannel):
                if id in cache:
                    concept.post = await client.get_channel(id).\
                        fetch_message(cache[id]).content
                else:
                    msg = await concept.get_first_message(thread)
                    cache[id], concept.post = msg.id, msg.content
                concept.source = concept.parse_source()
                if concept.source: sources.append(concept.source)
            concepts[id] = concept


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await check_channels()
    print("Done processing", cache)
    # write cache


def run_bot(): client.run(TOKEN)