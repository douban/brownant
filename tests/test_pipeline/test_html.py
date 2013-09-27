from __future__ import absolute_import, unicode_literals

from pytest import raises
from mock import patch, Mock

from brownant.pipeline.html import ElementTreeProperty, XPathTextProperty


# ElementTreeProperty

def test_etree_default_attr_name():
    etree = ElementTreeProperty()
    assert etree.attr_names["text_response_attr"] == "text_response"


@patch("lxml.html.fromstring")
def test_etree_general_parse_with_default(fromstring):
    mock = Mock()
    etree = ElementTreeProperty()
    etree.provide_value(mock)
    fromstring.assert_called_once_with(mock.text_response)


@patch("lxml.html.fromstring")
def test_etree_general(fromstring):
    mock = Mock()
    etree = ElementTreeProperty(text_response_attr="foo")
    etree.provide_value(mock)
    fromstring.assert_called_once_with(mock.foo)


# XPathTextProperty

def test_xpath_default_attr_name():
    with raises(TypeError):
        XPathTextProperty()

    text = XPathTextProperty(xpath="//path")
    assert text.xpath == "//path"
    assert text.attr_names["etree_attr"] == "etree"
    assert text.options["strip_spaces"] is False
    assert text.options["pick_mode"] == "join"
    assert text.options["joiner"] == " "


def test_xpath_without_spaces():
    mock = Mock()
    mock.tree.xpath.return_value = ["a", "b", "c"]

    # pick_mode: join
    text = XPathTextProperty(xpath="//path", etree_attr="tree",
                             pick_mode="join", joiner="|")
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with("//path")
    assert rv == "a|b|c"

    # pick_mode: first
    text = XPathTextProperty(xpath="//another-path", etree_attr="tree",
                             pick_mode="first")
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with("//another-path")
    assert rv == "a"


def test_xpath_with_striping_spaces():
    mock = Mock()
    mock.tree.xpath.return_value = [" a ", "\n b \n", "\n\n c  \t"]

    # strip_spaces and join
    text = XPathTextProperty(xpath="//foo-path", etree_attr="tree",
                             pick_mode="join", strip_spaces=True)
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with("//foo-path")
    assert rv == "a b c"

    # strip_spaces and first
    text = XPathTextProperty(xpath="//bar-path", etree_attr="tree",
                             pick_mode="first", strip_spaces=True)
    rv = text.provide_value(mock)
    mock.tree.xpath.assert_called_with("//bar-path")
    assert rv == "a"


def test_xpath_invalid_pick_mode():
    with raises(ValueError) as excinfo:
        text = XPathTextProperty(xpath="//foo-path", pick_mode="unknown")
        text.provide_value(Mock())
    assert "unknown" in repr(excinfo.value)
