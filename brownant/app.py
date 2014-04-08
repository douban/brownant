from __future__ import absolute_import, unicode_literals

from warnings import warn

from six import string_types
from six.moves import urllib
from werkzeug.utils import import_string
from werkzeug.urls import url_decode, url_encode
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect

from .request import Request
from .exceptions import NotSupported
from .utils import to_bytes_safe


class Brownant(object):
    """The app which could manage whole crawler system."""

    def __init__(self):
        self.url_map = Map(strict_slashes=False, host_matching=True,
                           redirect_defaults=False)

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
        url = self.validate_url(url)
        url_adapter = self.url_map.bind(server_name=url.hostname,
                                        url_scheme=url.scheme,
                                        path_info=url.path)
        query_args = url_decode(url.query)
        return url, url_adapter, query_args

    def validate_url(self, url):
        """Validate the :class:`~urllib.parse.ParseResult` object.

        This method will make sure the :meth:`~brownant.app.BrownAnt.parse_url`
        could work as expected even meet a unexpected URL string.

        :param url: the parsed url.
        :type url: :class:`~urllib.parse.ParseResult`
        """
        # fix up the non-ascii path
        url_path = to_bytes_safe(url.path)
        url_path = urllib.parse.quote(url_path, safe=b"/%")

        # fix up the non-ascii query
        url_query = to_bytes_safe(url.query)
        url_query = urllib.parse.quote(url_query, safe=b"?=&")

        url = urllib.parse.ParseResult(url.scheme, url.netloc, url_path,
                                       url.params, url_query, url.fragment)

        # validate the components of URL
        has_hostname = url.hostname is not None and len(url.hostname) > 0
        has_http_scheme = url.scheme in ("http", "https")
        has_path = not len(url.path) or url.path.startswith("/")

        if not (has_hostname and has_http_scheme and has_path):
            raise NotSupported("invalid url: %s" % repr(url))

        return url

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
        except RequestRedirect as e:
            new_url = "{0.new_url}?{1}".format(e, url_encode(query_args))
            return self.dispatch_url(new_url)

        try:
            handler = import_string(endpoint)
            request = Request(url=url, args=query_args)
            return handler(request, **kwargs)
        except RequestRedirect as e:
            return self.dispatch_url(e.new_url)

    def mount_site(self, site):
        """Mount a supported site to this app instance.

        :param site: the site instance be mounted.
        """
        if isinstance(site, string_types):
            site = import_string(site)
        site.play_actions(target=self)


class BrownAnt(Brownant):
    def __init__(self, *args, **kwargs):
        warn("The class name 'BrownAnt' has been deprecated. Please use "
             "'Brownant' instead.", DeprecationWarning)
        super(BrownAnt, self).__init__(*args, **kwargs)


def redirect(url):
    """Raise the :class:`~werkzeug.routing.RequestRedirect` exception to lead
    the app dispatching current request to another URL.

    :param url: the target URL.
    """
    raise RequestRedirect(url)
