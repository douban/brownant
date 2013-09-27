from __future__ import absolute_import, unicode_literals

from pytest import raises

from brownant.pipeline.base import PipelineProperty


def test_required_attrs():
    class SpamProperty(PipelineProperty):
        required_attrs = {"egg"}

        def provide_value(self, obj):
            return obj

    # valid
    spam_property = SpamProperty(egg=42)
    assert spam_property.egg == 42
    assert "egg" not in spam_property.options
    assert "egg" not in spam_property.attr_names
    with raises(AttributeError):
        spam_property.foo

    # invalid
    with raises(TypeError) as excinfo:
        spam_property = SpamProperty(spam=42)
    assert "egg" in repr(excinfo.value)


def test_attr_name():
    class SpamProperty(PipelineProperty):
        def prepare(self):
            self.attr_names.setdefault("egg_attr", "egg")

        def provide_value(self, obj):
            return self.get_attr(obj, "egg_attr")

    class Spam(object):
        def __init__(self, **kwargs):
            vars(self).update(kwargs)

    spam_a = SpamProperty(egg=42)
    assert spam_a.attr_names["egg_attr"] == "egg"
    assert spam_a.provide_value(Spam(egg=1024)) == 1024

    spam_b = SpamProperty(egg=42, egg_attr="foo_egg")
    assert spam_b.attr_names["egg_attr"] == "foo_egg"
    assert spam_b.provide_value(Spam(foo_egg=2048)) == 2048


def test_optional_attr():
    class SpamProperty(PipelineProperty):
        required_attrs = {"egg"}

        def provide_value(self, obj):
            return obj

    spam = SpamProperty(egg=41, foo=42, bar=43, aha_attr=44)
    assert spam.options["foo"] == 42
    assert spam.options["bar"] == 43
    assert "egg" not in spam.options
    assert "aha_attr" not in spam.options
