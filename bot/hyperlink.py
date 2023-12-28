from requests.exceptions import SSLError
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urlextract import URLExtract
from config import HTTP_allowed

extractor = URLExtract().find_urls

# media type if file, title/filename, parent message content/id (caption/jump-to link), $tag

class Hyperlink():
    def __init__(self, url, title=None, type=None):
        self.url = url
        self.title = title if title else self.get_title()
        self.type = type if type else self.get_type()

    def __str__(self): return self.url


    def get_title(self):
        if not self.url.startswith(('http://', 'https://')):
            self.url = 'https://' + self.url

        session = Session()
        retries = Retry(total=0,
                        backoff_factor=0,
                        status_forcelist=[ 500, 502, 503, 504 ],
                        allowed_methods=["HEAD", "GET", "OPTIONS"])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        try:
            response = session.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.string if soup.title else self.url
        except SSLError:
            if HTTP_allowed:
                self.url = self.url.replace('https://' , 'http://')
                try:
                    response = session.get(self.url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    return soup.title.string if soup.title else self.url
                except Exception:
                    return self.url
            else:
                return self.url
        except Exception:
            return self.url
    
    def get_type(self):
        if any([e in self.url for e in (".mp4", ".mp3", ".ogg", ".png", ".jpg", ".webp")]):
            return "media"
        return "site"