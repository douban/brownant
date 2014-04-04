from __future__ import absolute_import, unicode_literals


class Request(object):
    """The request object.

    :param url: the raw URL inputted from the dispatching app.
    :type url: :class:`urllib.parse.ParseResult`
    :param args: the query arguments decoded from query string of the URL.
    :type args: :class:`werkzeug.datastructures.MultiDict`
    """

    def __init__(self, url, args):
        self.url = url
        self.args = args

    def __repr__(self):
        return "Request(url={self.url}, args={self.args})".format(self=self)
