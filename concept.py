import appdirs
import json
from config import EXPORT_PATH
from os import makedirs
from os.path import exists, join
from hyperlink import Hyperlink


CACHE_DIR = appdirs.user_cache_dir(appname='Concept')


class Concept:
    """Represents a concept with links and media from a thread."""    


    def __init__(self, id, name, channel, category,
                 post=None, source=None, sites=None, media=None, pinned=None):
        if not sites: sites = []
        if not media: media = []
        if not pinned: pinned = []

        self.id = id
        self.name = name
        self.channel = channel
        self.category = category
        
        self.post = post
        self.source = source
        self.sites = sites
        self.media = media
        self.pinned = pinned

        self._str = None
        self._file = join(EXPORT_PATH, str(id)+'.md')


    def __str__(self):
        """Generate string of Concept contents as Markdown"""
        ret = f"[{self.category} >> #{self.channel}] "
        ret += "POST" if self.post else "THREAD"
        ret += f" {self.id}: {self.name} "
        if self.source:
            ret += f"\n\nSource Thread: [[{self.source}]]"

        if self.post:
            ret += '\n' + str(self.post)
        if self.pinned:
            ret += '\n- '.join((['\n\n## Pinned'] + self.pinned))
        
        return ret
    
    def __dict__(self):
        """Convert the Concept object to a dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'channel': self.channel,
            'category': self.category,
            'sites': [site.__dict__() for site in self.sites],
            'media': [media.__dict__() for media in self.media],
            'source': self.source
        }
        return data

    @classmethod
    def from_dict(cls, data):
        """Create a Concept object from a dictionary."""
        concept = cls(
            id=data.get('id'),
            name=data.get('name'),
            channel=data.get('channel'),
            category=data.get('category'),
            # other attributes...
        )
        concept.sites = [Hyperlink.from_dict(site) for site in data.get('sites', [])]
        concept.media = [Hyperlink.from_dict(media) for media in data.get('media', [])]
        concept.source = data['source']
        return concept

    def dont_generate_link_table(self):
        """Generate a table of links."""
        ret = '\n<table>\n<tr>\n'
        for count, link in enumerate(self.sites):
            if count % 3 == 0 and count != 0:  # between rows
                ret += '</tr>\n<tr>\n'
            ret += f'<td><a href="{link.url}">{link.title}</a></td>\n'
        ret += '</tr>\n</table>\n'
        return ret
    
    def dont_generate_media_table(self):
        """Generate a table of media."""
        ret = '\n<table>\n<tr>\n'
        for count, link in enumerate(self.media):
            if count % 3 == 0 and count != 0:  # between rows
                ret += '</tr>\n<tr>\n'
            if link.type.startswith("image/"):
                ret += f'<td><img src="{link.url}" width="200"/></td>\n'
            elif link.type.startswith("video/"):
                ret += f'<td><video src="{link.url}" width="200" controls></video></td>\n'
        ret += '</tr>\n</table>\n'
        return ret
    

    def export(self, cache=False):
        if EXPORT_PATH and exists(EXPORT_PATH):
            with open(self._file, 'w', encoding='utf-8') as fl:
                fl.write(self.__str__())

        if cache:
            makedirs(CACHE_DIR, exist_ok=True)
            with open(join(CACHE_DIR, str(self.id) + '.json'), 'w', encoding='utf-8') as fl:
                json.dump(self.__dict__(), fl)


    @classmethod
    def cached(cls, id):
        cache_file = join(CACHE_DIR, str(id)+'.json')
        if exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as fl:
                data = json.load(fl)
            return cls.from_dict(data)
        else:
            return None
        
