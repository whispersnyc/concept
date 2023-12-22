from bot.concept import Concept
from bot.config import TOKEN, CHANNELS
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

concepts, sources = {}, []


async def get_first_message(thread):
    # loop to the first message then return it
    async for msg in thread.history(limit=None): pass
    return msg.content


def get_source(post):
    try: # find <#...> at start (text channel id)
        if (txt := post.strip()).startswith('<#'):
            return int(txt[2:txt.index('>')])
    except Exception as e: return


async def check_channels():
    for channel_id in CHANNELS:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        # project posts
        if isinstance(channel, discord.ForumChannel):
            for thread in channel.threads:
                post = await get_first_message(thread)
                source = get_source(post)

                concepts[thread.id] = Concept(thread, thread.id, channel.category.name, channel.name, thread.name, post, source)
                if source: sources.append(source)

        # source threads
        elif isinstance(channel, discord.TextChannel):
            for thread in channel.threads:
                concepts[thread.id] = Concept(thread, thread.id, channel.category.name, channel.name, thread.name)
    
    print("Done processing")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await check_channels()


def run_bot(): client.run(TOKEN)