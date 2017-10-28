import os
from html_cluster.utils.common import is_html_page

tests_datadir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


def test_is_html_page():
    assert not is_html_page(tests_datadir + '/sample.pdf')
