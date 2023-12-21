from concept import Concept
from config import TOKEN, CHANNELS
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

concepts = {}


async def get_first_message(thread):
    async for post in thread.history(limit=None): pass
    return post


async def get_source(post):
    try:
        if (txt := post.content.strip()).startswith('<#'):
            return int(txt[2:txt.index('>')])
    except Exception:
        return


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
                concepts[thread.id] = Concept(thread.id, channel.category, channel.name, thread.name, post, source)
                print(concepts[thread.id])
 
        # source threads
        elif isinstance(channel, discord.TextChannel):
            for thread in channel.threads:
                concepts[thread.id] = Concept(thread.id, channel.category, channel.name, thread.name)
                print(concepts[thread.id])


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await check_channels()


if __name__ == "__main__":
    client.run(TOKEN)