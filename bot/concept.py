class Concept:
    def __init__(self, thread, thread_id, category_name, channel_name, thread_name, post=None, source=None):
        self.thread = thread
        self.id = thread_id
        self.category = category_name
        self.channel = channel_name
        self.name = thread_name
        self.post = post
        self.source = source

    def __str__(self):
        ret = f"[{self.category} >> #{self.channel}] {"POST" if self.post else "THREAD"} "
        ret += f"{self.id}: {self.name} "
        if self.source: ret += f"(src: {self.source})"

        return ret