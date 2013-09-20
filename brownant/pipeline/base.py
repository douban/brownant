from werkzeug.utils import cached_property


class PipelineProperty(cached_property):

    required_attrs = set()

    def __init__(self, **kwargs):
        super(PipelineProperty, self).__init__(self.provide_value)
        self.__name__ = None
        self.__module__ = None
        self.__doc__ = None

        self.attr_names = {}
        self.options = {}

        assigned_attrs = set()
        for name, value in kwargs.items():
            assigned_attrs.add(name)

            # names of attrs
            if name.endswith("_attr"):
                self.attr_names[name] = value
            # required attrs
            elif name in self.required_attrs:
                setattr(self, name, value)
            # optional attrs
            else:
                self.options[name] = value
        lacked_attrs = self.required_attrs - assigned_attrs
        if lacked_attrs:
            raise TypeError("required attrs %r" % ", ".join(lacked_attrs))

        self.prepare()

    def prepare(self):
        pass

    def get_attr(self, obj, name):
        attr_name = self.attr_names[name]
        return getattr(obj, attr_name)
