class Concept:
    def __init__(self, thread):
        self.thread = thread
        self.id = thread.id
        self.name = thread.name
        self.channel = thread.parent.name
        self.category = thread.parent.category.name

        self.post, self.source = None, None

        self.links, self.media = {}, {}

    @classmethod
    async def create(cls, thread, forum):
        concept = cls(thread)
        if forum: await concept.parse_post(thread, concept.id)
        return concept


    def __str__(self):
        ret = f"[{self.category} >> #{self.channel}] " + \
                ("POST" if self.post else "THREAD") + \
              f" {self.id}: {self.name} "
        if self.source: ret += f"(src: {self.source})"

        if self.post: ret += '\n\n## Post\n'+str(self.post)
        if self.links: ret += '\n\n## Links\n'+str(self.links)
        if self.media:
            ret += '\n\n## Media\n<table>\n<tr>\n'
            count = 0
            for sublist in self.media.values():
                for item in sublist:
                    if count % 3 == 0 and count != 0: # between rows
                        ret += '</tr>\n<tr>\n'
                    ret += f'<td><img src="{item}" width="200"/></td>\n'
                    count += 1
            ret += '</tr>\n</table>\n'
        return ret
    

    async def parse_post(self, thread, id):
        self.post = (await thread.fetch_message(id)).content
        try: # find/remove <#...> in post (text channel id)
            if (txt := self.post.strip()).startswith('<#'):
                source, txt = txt[2:].split('>', 1)
                source, self.post = int(source), txt.strip()
                self.source = source
        except Exception as e: return