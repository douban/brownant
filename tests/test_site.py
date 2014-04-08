from __future__ import absolute_import, unicode_literals

from pytest import fixture
from mock import Mock

from brownant import Site


@fixture
def sites():
    _sites = {
        "s1": Site("s1"),
        "s2": Site("s2"),
        "s3": Site("s3"),
    }
    return _sites


def test_new_site(sites):
    assert sites["s1"].name == "s1"
    assert sites["s2"].name == "s2"
    assert sites["s3"].name == "s3"

    assert sites["s1"].actions == []
    assert sites["s2"].actions == []
    assert sites["s3"].actions == []


def test_record_and_play_actions(sites):
    site = sites["s1"]

    mock = Mock()
    site.record_action("method_a", 10, "s", is_it=True)
    site.play_actions(target=mock)
    mock.method_a.assert_called_once_with(10, "s", is_it=True)


def test_route(sites):
    site = sites["s1"]

    @site.route("m.example.com", "/article/<int:article_id>")
    def handler(request, article_id):
        pass

    mock = Mock()
    site.play_actions(target=mock)
    mock.add_url_rule.assert_called_once_with(
        "m.example.com",
        "/article/<int:article_id>",
        __name__ + ":handler"
    )
