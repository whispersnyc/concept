class Concept:
    """Represents a concept with links and media from a thread."""

    def __init__(self, thread,id, name, channel, category, post=None, source=None):
        self.thread = thread
        self.id = id
        self.name = name
        self.channel = channel
        self.category = category

        self.post, self.source = post, source

        self.sites, self.media = [], []
        self._str = None


    @classmethod
    async def Discord_thread(cls, thread, from_forum):
        """Initialize Concept from Discord thread"""

        concept = cls(thread, thread.id, thread.name,
                      thread.parent.name, thread.parent.category.name)

        if from_forum: # fetch and set post/source
            concept.post = (await thread.fetch_message(thread.id)).content
            try: # find/remove <#...> in post (text channel id)
                if (txt := concept.post.strip()).startswith('<#'):
                    source, txt = txt[2:].split('>', 1)
                    source, concept.post = int(source), txt.strip()
                    concept.source = source
            except Exception as e: print(thread.name, e)
        
        return concept


    def __str__(self):
        if self._str: return self._str

        ret = f"[{self.category} >> #{self.channel}] " + \
                ("POST" if self.post else "THREAD") + \
              f" {self.id}: {self.name} "
        if self.source: ret += f"\n\nSource Thread: [[{self.source}]]"

        if self.post: ret += '\n\n## Post\n'+str(self.post)
        if self.sites:
            ret += '\n\n## Sites\n'
            for link in self.sites:
                ret += f"- [{link.title}]({link})\n"
        if self.media:
            ret += '\n\n## Media\n<table>\n<tr>\n'
            count = 0
            for link in self.media:
                if count % 3 == 0 and count != 0: # between rows
                    ret += '</tr>\n<tr>\n'
                if link.type.startswith("image/"):
                    ret += f'<td><img src="{link}" width="200"/></td>\n'
                elif link.type.startswith("video/"):
                    ret += f'<td><video src="{link}" width="200" controls></video></td>\n'
                count += 1
            ret += '</tr>\n</table>\n'
        
        self._str = ret
        return ret