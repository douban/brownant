from __future__ import absolute_import, unicode_literals

from mock import Mock
from pytest import raises

from brownant.exceptions import NotSupported
from brownant.pipeline.network import URLQueryProperty, TextResponseProperty


def test_url_query():
    mock = Mock()
    mock.request.args.get.return_value = "42"

    url_query = URLQueryProperty(name="value")
    rv = url_query.provide_value(mock)

    assert rv == "42"
    mock.request.args.get.assert_called_once_with("value", type=None)


def test_url_query_type():
    mock = Mock()
    mock.request.args.get.return_value = 42

    url_query = URLQueryProperty(name="value", type=int)
    rv = url_query.provide_value(mock)

    assert rv == 42
    mock.request.args.get.assert_called_once_with("value", type=int)


def test_url_query_required():
    mock = Mock()
    mock.request.args.get.return_value = None

    url_query = URLQueryProperty(name="value")  # default be required
    with raises(NotSupported):
        url_query.provide_value(mock)


def test_url_query_optional():
    mock = Mock()
    mock.request.args.get.return_value = None

    url_query = URLQueryProperty(name="d", type=float, required=False)
    rv = url_query.provide_value(mock)

    assert rv is None
    mock.request.args.get.assert_called_once_with("d", type=float)


def test_url_query_required_boundary_condition():
    mock = Mock()
    mock.request.args.get.return_value = 0

    url_query = URLQueryProperty(name="num")
    rv = url_query.provide_value(mock)

    assert rv == 0
    mock.request.args.get.assert_called_once_with("num", type=None)


def test_text_response():
    class HTTPError(Exception):
        pass

    response = Mock()
    response.text = "OK"
    response.raise_for_status.side_effect = [None, HTTPError()]

    mock = Mock()
    mock.url = "http://example.com"
    mock.http_client.get.return_value = response

    text = TextResponseProperty()
    rv = text.provide_value(mock)

    assert rv == "OK"
    response.raise_for_status.assert_called_once_with()
    mock.http_client.get.assert_called_once_with("http://example.com")

    with raises(HTTPError):
        text.provide_value(mock)
