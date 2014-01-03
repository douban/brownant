from __future__ import absolute_import, unicode_literals

from mock import Mock
from pytest import raises

from brownant import Dinergate


def test_basic():
    from requests import Session
    from werkzeug.utils import cached_property

    @cached_property
    def func_without_name(self):
        return [self]
    func_without_name.__name__ = None

    class FooDinergate(Dinergate):
        bar = func_without_name

    assert FooDinergate.bar.__name__ == "bar"

    mock_request = Mock()
    ant = FooDinergate(mock_request)

    assert ant.request is mock_request
    assert isinstance(ant.http_client, Session)
    assert ant.bar == [ant]


def test_custom_kwargs():
    mock_request = Mock()
    ant = Dinergate(mock_request, foo=42, bar="hello")
    assert ant.foo == 42
    assert ant.bar == "hello"


def test_custom_http_client():
    mock_request = Mock()
    mock_http_client = Mock()
    ant = Dinergate(mock_request, mock_http_client)

    ant.request.args.get("name", type=str)
    mock_request.args.get.assert_called_once_with("name", type=str)

    ant.http_client.post("http://example.com")
    mock_http_client.post.assert_called_once_with("http://example.com")


def test_url_template():
    class FooDinergate(Dinergate):
        foo = 42
        bar = "page"

        URL_TEMPLATE = "http://example.com/{self.bar}/{self.foo}"

    ant = FooDinergate(request=Mock(), http_client=Mock())
    assert ant.url == "http://example.com/page/42"

    dead_ant = Dinergate(request=Mock(), http_client=Mock())
    with raises(NotImplementedError):
        dead_ant.url
