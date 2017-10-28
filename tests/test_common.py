import os

from html_cluster.utils.common import FileUrlsReader

tests_datadir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


def test_file_reader():
    reader = FileUrlsReader(tests_datadir + '/urls-empty-lines.txt')
    assert 5 == len(list(reader.read()))
