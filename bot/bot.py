from bot.concept import Concept
from bot.config import TOKEN, CHANNELS
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

concepts, sources = {}, []


async def check_channels():
    for channel_id in CHANNELS:
        channel = client.get_channel(int(channel_id))
        if channel is None:
            print(f"Could not find channel {channel_id}")
            continue

        for thread in channel.threads:
            concept = concepts[thread.id] = Concept(thread)
            if isinstance(channel, discord.ForumChannel):
                concept.post = await concept.get_first_message()
                concept.source = concept.parse_source()
                if concept.source: sources.append(concept.source)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await check_channels()
    print("Done processing")


def run_bot(): client.run(TOKEN)