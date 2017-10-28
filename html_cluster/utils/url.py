import re


def is_url(url):
    regex = re.compile(
        # http:// or https://
        r'^(?:http|ftp)s?://'
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        # localhost...
        r'localhost|'
        # ...or ip
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        # optional port
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if regex.match(url):
        return True
    return False
