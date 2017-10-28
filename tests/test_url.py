from html_cluster.utils.url import is_url


def test_is_url():
    assert is_url('http://example.com')
    assert is_url('http://example.com:8080')
    assert not is_url('text')
