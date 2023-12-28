from requests.exceptions import SSLError
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

def get_title(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    session = Session()
    retries = Retry(total=0,
                    backoff_factor=0,
                    status_forcelist=[ 500, 502, 503, 504 ],
                    allowed_methods=["HEAD", "GET", "OPTIONS"])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.title.string if soup.title else url
    except SSLError:
        return url