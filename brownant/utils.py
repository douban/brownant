from six import text_type
from six.moves import urllib

from .exceptions import NotSupported


__all__ = ("to_bytes_safe", "clean_up_url")


def to_bytes_safe(text, encoding="utf-8"):
    """Convert the input value into bytes type.

    If the input value is string type and could be encode as UTF-8 bytes, the
    encoded value will be returned. Otherwise, the encoding has failed, the
    origin value will be returned as well.

    :param text: the input value which could be string or bytes.
    :param encoding: the expected encoding be used while converting the string
                     input into bytes.
    :rtype: :class:`~__builtin__.bytes`
    """
    if not isinstance(text, (bytes, text_type)):
        raise TypeError("must be string type")

    if isinstance(text, text_type):
        return text.encode(encoding)

    return text


def clean_up_url(url):
    """Clean up the :class:`~urllib.parse.ParseResult` object.

    This function will make sure the :meth:`~brownant.app.BrownAnt.parse_url`
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
