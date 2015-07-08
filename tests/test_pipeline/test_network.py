from __future__ import absolute_import, unicode_literals

from mock import Mock, patch
from pytest import raises

from brownant.exceptions import NotSupported
from brownant.pipeline.network import (HTTPClientProperty, URLQueryProperty,
                                       TextResponseProperty, ResponseProperty,
                                       JSONResponseProperty)


def test_http_client():
    dinergate = Mock()
    with patch("requests.Session") as Session:
        instance = Session.return_value
        http_client = HTTPClientProperty(session_class=Session)
        assert http_client.provide_value(dinergate) is instance
        Session.assert_called_once_with()


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


def test_base_response():
    response = Mock()
    response.text = "OK"

    mock = Mock()
    mock.url = "http://example.com"
    mock.http_client.request.return_value = response

    response = ResponseProperty()
    with raises(KeyError):
        response.provide_value(mock)


def test_text_response():
    class HTTPError(Exception):
        pass

    response = Mock()
    response.text = "OK"
    response.raise_for_status.side_effect = [None, HTTPError()]

    mock = Mock()
    mock.url = "http://example.com"
    mock.http_client.request.return_value = response

    text = TextResponseProperty(method="POST")
    rv = text.provide_value(mock)

    assert rv == "OK"
    response.raise_for_status.assert_called_once_with()
    mock.http_client.request.assert_called_once_with(
        method="POST", url="http://example.com")

    with raises(HTTPError):
        text.provide_value(mock)


def test_json_response():
    class HTTPError(Exception):
        pass

    response = Mock()
    response.json.return_value = {'a': 1, 'b': {'c': 2, 'd': 3}}
    response.raise_for_status.side_effect = [None, HTTPError()]

    mock = Mock()
    mock.url = "http://example.com"
    mock.http_client.request.return_value = response

    json = JSONResponseProperty(method="POST")
    rv = json.provide_value(mock)

    assert rv == {
        'a': 1,
        'b': {
            'c': 2,
            'd': 3
        }
    }
    response.raise_for_status.assert_called_once_with()
    mock.http_client.request.assert_called_once_with(
        method="POST", url="http://example.com")

    with raises(HTTPError):
        json.provide_value(mock)
