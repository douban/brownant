from __future__ import absolute_import, unicode_literals


class BrownantException(Exception):
    """The base exception of the Brownant framework."""


class NotSupported(BrownantException):
    """The given URL or other identity is from a platform which not support.

    This exception means any url rules of the app which matched the URL could
    not be found.
    """
