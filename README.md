# Concept
An experimental idea, project and resource management system using Discord and a custom WebUI

NOTE: This project has been abandoned for a privacy-conscious alternative like Praxis but still functional as of 4/5/25

The idea
- Post all your ideas in an `#ideas` text channel
- Use [EasyThreads bot](https://docs.easysystems.live/docs/easythreads/intro) to automatically create threads for those ideas
- Quickly drop any images, videos, links, files and further ideas into the respective thread
- For ideas that develop into full-on projects, make a post in a Forum channel like `#projects`. Paste a link to the source thread at the very beginning of your post to sync them (right click on thread -> Copy Link)
- Browse your resources and most important project details for all your ideas/projects in one place using Concept
- Use Discord's Role/Permission systems to selectively grant read/write access to people for feedback/contributions

What does Concept do?
- Automatically extracts links and imgs/vids from your Discord posts/thread to display them all in a compact easy-to-access manner (topmost post message and links on left, images/videos in 3 columns on right)
- Add a link to a thread at the very start of your post (type # in Discord input box and type the name or paste the share link) for it to be treated as the "source thread" so all of it's links/files will be added together with the post's
- Send an idea to a text channel using the input box up top
- Refresh button for rescanning a specific or all channels
- Markdown export and cache for faster initial load (these may be buggy)
- Fetch link titles feature may slow down processing and sometimes works counterproductively by generalizing links, ex. "Reddit - The heart of the internet"

Why?
- Discord is extremely popular (easy multi-user collaboration)
- supports Markdown formatting (Miro somehow doesn't)
- multiplatform with community-modded clients available
- loads/works faster than a plugin-filled Obsidian on mobile (before the horrid Discord update)
- theoretically unlimited storage space ([proof](https://www.youtube.com/watch?v=c_arQ-6ElYI))


## Project Structure

Discord.py bot retrieves posts/thread from config.py's CHANNELS list.  
`bot/` contains `bot.py`

Bottle WebUI displays concept data by converting markdown to HTML  
`webui/` contains `app.py`

Concept class holds thread info, links/media Hyperlinks and markdown __str__()  
Hyperlink class contains url, url title, mimetype if file  
root contains `concept.py`, `config.py`, `hyperlink.py`, `main.py`


## Installation

1. Clone the repository
2. Create a virtual environment and activate it:
```python
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```
3. Install dependencies:
```python
pip install -r requirements.txt
```
4. Rename config.py.example to config.py and configure:
   - Get your Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)
   - Enable Developer Mode in Discord to copy channel IDs
   - Add channel IDs to `CHANNELS` list
   - Set `IDEA_CHANNEL` ID for the ideas feature
   - Configure other optional settings as needed

5. Run the application:
```python
python main.py
```

## Usage

1. Access the web interface at `localhost:8080`
2. Use the top input box to send new ideas to your Discord channel
3. Click refresh button to rescan specific channels or all channels
4. Click on any concept to view its details, links and media

## Configuration Options

- `LAZY_LOADING`: Disable to process all messages at startup
- `EXPORT_PATH`: Enable Markdown export by setting a valid path
- `CACHE`: Enable caching for faster initial load
- `FETCH_LINK_TITLES`: Enable to replace links with webpage titles
- `HTTP_ALLOWED`: Allow fallback to HTTP when HTTPS fails