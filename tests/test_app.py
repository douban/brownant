from __future__ import absolute_import, unicode_literals

from pytest import fixture, raises
from mock import patch

from brownant.app import BrownAnt
from brownant.exceptions import NotSupported


class StubEndpoint(object):

    name = __name__ + ".StubEndpoint"

    def __init__(self, request, id_):
        self.request = request
        self.id_ = id_


@fixture
def app():
    _app = BrownAnt()
    _app.add_url_rule("m.example.com", "/item/<int:id_>", StubEndpoint.name)
    return _app


def test_new_app(app):
    assert isinstance(app, BrownAnt)
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
