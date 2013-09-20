from six import with_metaclass
from werkzeug.utils import cached_property
from requests import Session


class DinergateType(type):

    def __new__(metacls, name, bases, members):
        cls = type.__new__(metacls, name, bases, members)
        for name in dir(cls):
            value = getattr(cls, name)
            if isinstance(value, cached_property) and not value.__name__:
                value.__name__ = name
                value.__module__ = cls.__module__
        return cls


class Dinergate(with_metaclass(DinergateType)):
    """The simple pipeline for crawling given site."""

    URL_TEMPLATE = None

    def __init__(self, request, http_client=None, **kwargs):
        self.request = request
        self.http_client = http_client or Session()
        # assign arguments from URL pattern
        vars(self).update(kwargs)

    @property
    def url(self):
        if not self.URL_TEMPLATE:
            raise NotImplemented
        return self.URL_TEMPLATE.format(self=self)
