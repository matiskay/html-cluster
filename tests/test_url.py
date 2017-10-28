import os

from html_cluster.utils.url import is_url, FileUrlsReader


def test_is_url():
    assert is_url('http://example.com')
    assert is_url('http://example.com:8080')
    assert not is_url('text')


tests_datadir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


def test_file_reader():
    reader = FileUrlsReader(tests_datadir + '/urls-empty-lines.txt')
    assert 5 == len(list(reader.read()))
