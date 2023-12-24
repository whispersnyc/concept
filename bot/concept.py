class Concept:
    def __init__(self, thread):
        self.thread = thread
        self.id = thread.id
        self.name = thread.name
        self.channel = thread.parent.name
        self.category = thread.parent.category.name
        self.post, self.source = None, None

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

        return ret
    

    async def parse_post(self, thread, id):
        self.post = (await thread.fetch_message(id)).content
        try: # find/remove <#...> in post (text channel id)
            if (txt := self.post.strip()).startswith('<#'):
                source, txt = txt[2:].split('>', 1)
                source, self.post = int(source), txt.strip()
                self.source = source
        except Exception as e: return