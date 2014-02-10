from __future__ import absolute_import, unicode_literals

from pytest import fixture, raises
from mock import patch

from brownant import Brownant, redirect
from brownant.exceptions import NotSupported


class StubEndpoint(object):

    name = __name__ + ".StubEndpoint"

    def __init__(self, request, id_, **kwargs):
        self.request = request
        self.id_ = id_


def redirect_endpoint(request, **kwargs):
    should_redirect = (request.args.get("r") == "1")
    if should_redirect:
        return redirect("http://redirect.example.com/42?id=24")
    return kwargs, request


redirect_endpoint.__qualname__ = __name__ + "." + redirect_endpoint.__name__


@fixture
def app():
    _app = Brownant()
    _app.add_url_rule("m.example.com", "/item/<int:id_>", StubEndpoint.name)
    _app.add_url_rule("m.example.co.jp", "/item/<id_>", StubEndpoint.name)
    return _app


def test_new_app(app):
    assert isinstance(app, Brownant)
    assert callable(app.add_url_rule)
    assert callable(app.dispatch_url)
    assert callable(app.mount_site)


def test_match_url(app):
    stub = app.dispatch_url("http://m.example.com/item/289263?page=1&q=t")

    assert stub.id_ == 289263
    assert stub.request.args["page"] == "1"
    assert stub.request.args["q"] == "t"

    with raises(KeyError):
        stub.request.args["other"]

    assert repr(stub.request).startswith("Request(")
    assert repr(stub.request).endswith(")")
    assert "url=" in repr(stub.request)
    assert "m.example.com" in repr(stub.request)
    assert "/item/289263" in repr(stub.request)
    assert "args=" in repr(stub.request)

    assert stub.request.url.scheme == "http"
    assert stub.request.url.hostname == "m.example.com"
    assert stub.request.url.path == "/item/289263"

    assert stub.request.args.get("page", type=int) == 1
    assert stub.request.args["q"] == "t"


def test_match_url_without_redirect(app):
    app.add_url_rule("detail.example.com", "/item/<int:id_>",
                     StubEndpoint.name, defaults={"p": "a"})
    app.add_url_rule("mdetail.example.com", "/item/<int:id_>",
                     StubEndpoint.name, defaults={"p": "a"})

    stub = app.dispatch_url("http://detail.example.com/item/12346?page=6")
    assert stub.id_ == 12346
    assert stub.request.args.get("page", type=int) == 6

    stub = app.dispatch_url("http://mdetail.example.com/item/12346?page=6")
    assert stub.id_ == 12346
    assert stub.request.args.get("page", type=int) == 6


def test_match_url_with_redirect(app):
    app.add_url_rule("m.example.com", "/42", StubEndpoint.name,
                     redirect_to="item/42")

    stub = app.dispatch_url("http://m.example.com/item/42/?page=6")
    assert stub.id_ == 42
    assert stub.request.args.get("page", type=int) == 6

    stub = app.dispatch_url("http://m.example.com/42?page=6")
    assert stub.id_ == 42
    assert stub.request.args.get("page", type=int) == 6

    stub = app.dispatch_url("http://m.example.com/item/42/")
    assert stub.id_ == 42
    with raises(KeyError):
        stub.request.args["page"]

    stub = app.dispatch_url("http://m.example.com/42")
    assert stub.id_ == 42
    with raises(KeyError):
        stub.request.args["page"]


def test_match_url_and_handle_user_redirect(app):
    domain = "redirect.example.com"
    app.add_url_rule(domain, "/<id>", redirect_endpoint.__qualname__)

    kwargs, request = app.dispatch_url("http://{0}/123?id=5".format(domain))
    assert kwargs == {"id": "123"}
    assert request.args["id"] == "5"

    kwargs, request = app.dispatch_url("http://{0}/1?id=5&r=1".format(domain))
    assert kwargs == {"id": "42"}
    assert request.args["id"] == "24"


def test_match_non_ascii_url(app):
    url = u"http://m.example.co.jp/item/\u30de\u30a4\u30f3\u30c9"
    stub = app.dispatch_url(url)

    encoded_path = "/item/%E3%83%9E%E3%82%A4%E3%83%B3%E3%83%89"
    assert stub.request.url.scheme == "http"
    assert stub.request.url.hostname == "m.example.co.jp"
    assert stub.request.url.path == encoded_path


def test_match_non_ascii_query(app):
    url = u"http://m.example.co.jp/item/test?src=\u63a2\u9669&r=1"
    stub = app.dispatch_url(url)

    assert stub.request.url.scheme == "http"
    assert stub.request.url.hostname == "m.example.co.jp"
    assert stub.request.url.path == "/item/test"
    assert stub.request.url.query == "src=%E6%8E%A2%E9%99%A9&r=1"

    assert set(stub.request.args) == {"src", "r"}
    assert stub.request.args["src"] == u"\u63a2\u9669"
    assert stub.request.args["r"] == "1"


def test_match_unexcepted_url(app):
    unexcepted_url = "http://m.example.com/category/19352"

    with raises(NotSupported) as error:
        app.dispatch_url(unexcepted_url)

    # ensure the exception information is useful
    assert unexcepted_url in str(error)

    # ensure the rule could be added in runtime
    app.add_url_rule("m.example.com", "/category/<int:id_>", StubEndpoint.name)
    stub = app.dispatch_url(unexcepted_url)
    assert stub.id_ == 19352
    assert len(stub.request.args) == 0


def test_match_invalid_url(app):
    # empty string
    with raises(NotSupported) as error:
        app.dispatch_url("")
    assert "invalid" in str(error)

    # has not hostname
    with raises(NotSupported) as error:
        app.dispatch_url("/")
    assert "invalid" in str(error)

    # has not hostname and path
    with raises(NotSupported) as error:
        app.dispatch_url("\\")
    assert "invalid" in str(error)

    # not http scheme
    with raises(NotSupported) as error:
        app.dispatch_url("ftp://example.com")
    assert "invalid" in str(error)

    # valid input
    with raises(NotSupported) as error:
        app.dispatch_url("http://example.com")
    assert "invalid" not in str(error)

    with raises(NotSupported) as error:
        app.dispatch_url("https://example.com")
    assert "invalid" not in str(error)


foo_site = object()


def test_mount_site(app):
    foo_site_name = __name__ + ".foo_site"
    with patch(foo_site_name):
        app.mount_site(foo_site)
        foo_site.play_actions.assert_called_with(target=app)


def test_mount_site_by_string_name(app):
    foo_site_name = __name__ + ".foo_site"
    with patch(foo_site_name):
        app.mount_site(foo_site_name)
        foo_site.play_actions.assert_called_with(target=app)
