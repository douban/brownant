from __future__ import absolute_import, unicode_literals


class Request(object):
    """The crawling request object.

    :param args: the query arguments decoded from query string of the URL.
    """

    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return "Request(args={self.args})".format(self=self)
