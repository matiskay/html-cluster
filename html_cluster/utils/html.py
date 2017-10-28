import codecs
import lxml.html


def is_html_page_from_string(html):
    return lxml.html.fromstring(html).find('.//*') is not None


def is_html_page(file_path):
    with codecs.open(file_path, encoding='utf-8', errors='ignore') as file_html:
        html = file_html.read()
        return is_html_page_from_string(html)
