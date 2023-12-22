class Concept:
    def __init__(self, thread):
        self.thread = thread
        self.id = thread.id
        self.name = thread.name
        self.channel = thread.parent.name
        self.category = thread.parent.category.name
        self.post, self.source = None, None


    def __str__(self):
        ret = f"[{self.category} >> #{self.channel}] {"POST" if self.post else "THREAD"} "
        ret += f"{self.id}: {self.name} "
        if self.source: ret += f"(src: {self.source})"

        return ret
    

    async def get_first_message(self, thread):
        # loop to the first message then return it
        async for msg in thread.history(limit=None): pass
        return msg.content


    def parse_source(self, post):
        try: # find <#...> at start (text channel id)
            if (txt := post.strip()).startswith('<#'):
                return int(txt[2:txt.index('>')])
        except Exception as e: return