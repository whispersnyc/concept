import requests
from requests.exceptions import SSLError
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urlextract import URLExtract
from config import HTTP_ALLOWED, FETCH_LINK_TITLES
import mimetypes
from urllib.parse import urlparse

extractor = URLExtract().find_urls


class Hyperlink():
    title_cache = {}

    def __init__(self, url, title=None, type=None, source=None):
        self.url = url
        self.title = title
        self.type = type if type else self.get_type()
        self.source = source
        
        if not title or title == url:
            self.title = self.get_title()
        

    def __str__(self): return self.url

    def __dict__(self):
        return {
            "url": self.url,
            "title": self.title,
            "type": self.type,
            "source": self.source
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['url'], data['title'], data['type'], data['source'])
    

    def get_title(self):
        """Fetches the title of the webpage at the URL."""
        if not FETCH_LINK_TITLES: return self.url

        if self.url in Hyperlink.title_cache:
            return Hyperlink.title_cache[self.url]

        if not self.url.startswith(('http://', 'https://')):
            self.url = 'https://' + self.url

        session = Session()
        retries = Retry(
            total=5,  # Increase the total number of retry attempts
            backoff_factor=0.1,  # Add a delay between retry attempts
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        adapter = HTTPAdapter(max_retries=0)  # Set max_retries to 0
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        try:
            #response = session.get(self.url)
            try:
                response = session.get(self.url)
                soup = BeautifulSoup(response.text, 'html.parser')
                Hyperlink.title_cache[self.url] = soup.title.string if soup.title else self.url
            except requests.exceptions.ConnectionError as e:
                print(f"Error connecting to {self.url}: {e}")
        except (SSLError, requests.exceptions.RetryError):
            if HTTP_ALLOWED:
                self.url = self.url.replace('https://', 'http://')
                try:
                    response = session.get(self.url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    Hyperlink.title_cache[self.url] = soup.title.string if soup.title else self.url
                except Exception as e:
                    print(f"Failed to get title for {self.url}: {e}")
                    Hyperlink.title_cache[self.url] = self.url


        
        try:
            response = session.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')
            Hyperlink.title_cache[self.url] = soup.title.string if soup.title else self.url
        except (requests.exceptions.ConnectionError, SSLError, requests.exceptions.RetryError) as e:
            print(f"Error connecting to {self.url}: {e}")
            Hyperlink.title_cache[self.url] = self.url
        
        try:
            return Hyperlink.title_cache[self.url]
        except KeyError:
            return self.url


    def get_type(self):
        parsed_url = urlparse(self.url)
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        type, encoding = mimetypes.guess_type(clean_url)
        if type is None and clean_url.endswith('.webp'):
            return 'image/webp'
        return type if type else "site"