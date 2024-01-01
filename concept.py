import re
from config import EXPORT_PATH
from os.path import exists, join
from hyperlink import Hyperlink


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
        self._file = join(EXPORT, str(id)+'.md')


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
    

    def export(self):
        if EXPORT_PATH and exists(EXPORT_PATH):
            with open(self._file, 'w', encoding='utf-8') as fl:
                fl.write(self.__str__())
    

    @classmethod
    def parse_markdown(cls, id):
        with open(join(EXPORT, str(id)+'.md'), 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the concept
        concept_match = re.match(r'\[(.*?) >> #(.*?)] (POST|THREAD) (\d+): (.*?) ', content)
        category, channel, post_or_thread, id, name = concept_match.groups()
        from_forum = post_or_thread == 'POST'

        # Parse the source thread
        source_match = re.search(r'Source Thread: \[\[(.*?)\]\]', content)
        source = source_match.group(1) if source_match else None

        # Parse the sites
        sites = []
        sites_section = re.search(r'## Sites\n(.*?)\n\n', content, re.DOTALL)
        if sites_section:
            sites_matches = re.findall(r'- \[(.*?)\]\((.*?)\)', sites_section.group(1))
            for title, url in sites_matches:
                sites.append(Hyperlink(title, url))  # assuming Hyperlink takes title and url as arguments

        # Parse the media
        media = []
        media_section = re.search(r'## Media\n<table>\n(.*?)\n</table>', content, re.DOTALL)
        if media_section:
            media_matches = re.findall(r'src="(.*?)"', media_section.group(1))
            for url in media_matches:
                media.append(Hyperlink(url, url))  # assuming Hyperlink takes title and url as arguments

        return Concept(id, name, channel, category, from_forum, source, sites, media)