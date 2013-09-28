from __future__ import absolute_import, unicode_literals


class Site(object):
    """The site supported object which could be mounted to app instance.

    :param name: the name of the supported site.
    """

    def __init__(self, name):
        self.name = name
        self.actions = []

    def record_action(self, method_name, *args, **kwargs):
        """Record the method-calling action.

        The actions expect to be played on an target object.

        :param method_name: the name of called method.
        :param args: the general arguments for calling method.
        :param kwargs: the keyword arguments for calling method.
        """
        self.actions.append((method_name, args, kwargs))

    def play_actions(self, target):
        """Play record actions on the target object.

        :param target: the target which recive all record actions, is a brown
                       ant app instance normally.
        :type target: :class:`brownant.site.Site`
        """
        for method_name, args, kwargs in self.actions:
            method = getattr(target, method_name)
            method(*args, **kwargs)

    def route(self, host, rule, **options):
        """The decorator to register wrapped function to the brown ant app.

        The parameters of this method is compatible with the
        :meth:`BrownAnt.add_url_rule` method.

        :param host: the limited host name.
        :param rule: the URL path rule as string.
        :param options: the options to be forwarded to the
                        :class:`~werkzeug.routing.Rule` object.
        """
        def decorator(func):
            endpoint = "{func.__module__}:{func.__name__}".format(func=func)
            self.record_action("add_url_rule", host, rule, endpoint, **options)
            return func
        return decorator
