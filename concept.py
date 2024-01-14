import appdirs
import pickle
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
            ret += '\n\n## Post\n' + str(self.post)
        if self.pinned:
            ret += '\n- '.join((['\n\n## Pinned'] + self.pinned))
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
    

    def export(self, cache=False):
        if EXPORT_PATH and exists(EXPORT_PATH):
            with open(self._file, 'w', encoding='utf-8') as fl:
                fl.write(self.__str__())

        if cache:
            makedirs(CACHE_DIR, exist_ok=True)
            with open(join(CACHE_DIR, str(self.id) + '.pickle'), 'wb') as fl:
                pickle.dump(self, fl)


    @classmethod
    def cached(cls, id):
        cache_file = join(CACHE_DIR, str(id)+'.pickle')
        if exists(cache_file):
            with open(cache_file, 'rb') as fl:
                return pickle.load(fl)
        else: return None