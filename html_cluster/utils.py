from urllib.parse import urlparse
from hashlib import md5

import lxml.html
# Check if the html is an html page.


def is_html_page(file_path):
    with open(file_path) as file_html:
        html = file_html.read()
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
