# Concept

A project management WebUI using Discord. Why?
- Discord is extremely popular
    - accessible for outside contribution
    - also downside since joined servers are too common thus quickly forgotten
- supports Markdown formatting, though (Miro doesn't...)
- multiplatform with community-modded clients available
- theoretically unlimited storage space ([proof](https://www.youtube.com/watch?v=c_arQ-6ElYI))
    - "if you don't pay for it, you are the product"
- 


## Maze Map

Discord.py bot retrieves posts/thread from config.py's CHANNELS list.
bot/ contains [bot.py]

Bottle WebUI displays concept data by converting markdown to HTML
webui/ contains [app.py]

Concept class holds thread info, links/media Hyperlinks and markdown __str__()
Hyperlink class contains url, url title, mimetype if file
root contains [concept.py], [config.py], [hyperlink.py], [main.py]


## Concepts

use view transitions to smoothly animate between a mojo-generated blog site, bottle.py site (this) and standard github pages static site? (src: fireship)

