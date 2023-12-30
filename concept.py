class Concept:
    """Represents a concept with links and media from a thread."""    


    def __init__(self, id, name, channel, category,
                 post=None, source=None, sites=None, media=None):
        if not sites: sites = []
        if not media: media = []

        self.id = id
        self.name = name
        self.channel = channel
        self.category = category
        
        self.post = post
        self.source = source
        self.sites = sites
        self.media = media

        self._str = None


    def __str__(self):
        """Generate string of Concept contents as Markdown"""
        ret = f"[{self.category} >> #{self.channel}] "
        ret += "POST" if self.post else "THREAD"
        ret += f" {self.id}: {self.name} "
        if self.source:
            ret += f"\n\nSource Thread: [[{self.source}]]"

        if self.post:
            ret += '\n\n## Post\n' + str(self.post)
        if self.sites:
            ret += '\n\n## Sites\n'
            for link in self.sites:
                ret += f"- [{link.title}]({link})\n"
        if self.media:
            ret += self._generate_media_table()
        
        return ret


    def _generate_media_table(self):
        ret = '\n\n## Media\n<table>\n<tr>\n'
        for count, link in enumerate(self.media):
            if count % 3 == 0 and count != 0:  # between rows
                ret += '</tr>\n<tr>\n'
            if link.type.startswith("image/"):
                ret += f'<td><img src="{link}" width="200"/></td>\n'
            elif link.type.startswith("video/"):
                ret += f'<td><video src="{link}" width="200" controls>\
                         </video></td>\n'
        ret += '</tr>\n</table>\n'
        return ret