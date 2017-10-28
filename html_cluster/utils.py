import re
from urllib.parse import urlparse
from hashlib import md5

import lxml.html
# Check if the html is an html page.


def is_html_page(file_path):
    with open(file_path) as file_html:
        html = file_html.read()
        return lxml.html.fromstring(html).find('.//*') is not None


def is_html_page_from_string(html):
    return lxml.html.fromstring(html).find('.//*') is not None


def make_id(text):
    m = md5(text.encode('utf-8'))
    return m.hexdigest()[:5]


def get_base_path(url):
    return urlparse(url).netloc


def file_name(url, text):
    return get_base_path(url) + '.' + make_id(text)


def similarity_color(similarity_value):
    if 0 <= similarity_value < 50:
        return 'red'
    elif 50 <= similarity_value < 70:
        return 'yellow'
    return 'green'


def is_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if regex.match(url):
        return True
    return False

# This class parse a file
# Only valid urls
# Non spaces
class FileUrlsReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

            for line in lines:
                url = line.replace('\n', '').strip()
                url = url.strip()
                if not is_url(url):
                    continue
                yield url
