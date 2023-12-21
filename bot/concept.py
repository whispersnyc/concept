class Concept:
    def __init__(self, thread_id, category, channel_name, thread_name, post=None, source=None):
        self.thread_id = thread_id
        self.category = category
        self.channel_name = channel_name
        self.thread_name = thread_name
        self.post = post
        self.source = source

    def __str__(self):
        return f"[{self.category} >> #{self.channel_name}] {"POST" if self.post else "THREAD"} {self.thread_id}: {self.thread_name}"