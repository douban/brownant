from __future__ import absolute_import, unicode_literals

from six import string_types
from six.moves import urllib
from werkzeug.utils import import_string
from werkzeug.urls import url_decode
from werkzeug.routing import Map, Rule, NotFound

from .request import Request
from .exceptions import NotSupported


class BrownAnt(object):
    """The app which could manage whole crawler system."""

    def __init__(self):
        self.url_map = Map(strict_slashes=False, host_matching=True)

    def add_url_rule(self, host, rule_string, endpoint, **options):
        """Add a url rule to the app instance.

        The url rule is the same with Flask apps and other Werkzeug apps.

        :param host: the matched hostname. e.g. "www.python.org"
        :param rule_string: the matched path pattern. e.g. "/news/<int:id>"
        :param endpoint: the endpoint name as a dispatching key such as the
                         qualified name of the object.
        """
        rule = Rule(rule_string, host=host, endpoint=endpoint, **options)
        self.url_map.add(rule)

    def parse_url(self, url_string):
        """Parse the URL string with the url map of this app instance.

        :param url_string: the origin URL string.
        :returns: the tuple as `(url, url_adapter, query_args)`, the url is
                  parsed by the standard library `urlparse`, the url_adapter is
                  from the werkzeug bound URL map, the query_args is a
                  multidict from the werkzeug.
        """
        url = urllib.parse.urlparse(url_string)
        url_adapter = self.url_map.bind(server_name=url.hostname,
                                        url_scheme=url.scheme,
                                        path_info=url.path)
        query_args = url_decode(url.query)
        return url, url_adapter, query_args

    def dispatch_url(self, url_string):
        """Dispatch the URL string to the target endpoint function.

        :param url_string: the origin URL string.
        :returns: the return value of calling dispatched function.
        """
        url, url_adapter, query_args = self.parse_url(url_string)

        try:
            endpoint, kwargs = url_adapter.match()
        except NotFound:
            raise NotSupported(url_string)

        handler = import_string(endpoint)
        request = Request(url=url, args=query_args)
        return handler(request, **kwargs)

    def mount_site(self, site):
        """Mount a supported site to this app instance.

        :param site: the site instance be mounted.
        """
        if isinstance(site, string_types):
            site = import_string(site)
        site.play_actions(target=self)
