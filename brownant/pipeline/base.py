from werkzeug.utils import cached_property


class PipelineProperty(cached_property):
    """The base class of pipeline properties.

    There are three kinds of initial parameters.

    - The required attribute. If a keyword argument's name was defined in
      :attr:`~brownant.pipeline.base.PipelineProperty.required_attrs`, it will
      be assigned as an instance attribute.

    - The attr_name. It is the member of
      :attr:`~brownant.pipeline.base.PipelineProperty.attr_names`, whose name
      always end with `_attr`, such as `text_attr`.

    - The option. It will be placed at an instance owned :class:`dict` named
      :attr:`~brownant.pipeline.base.PipelineProperty.options`. The subclasses
      could set default option value in the
      :meth:`~brownant.pipeline.base.PipelineProperty.prepare`.

    A workable subclass of :class:`~brownant.pipeline.base.PipelineProperty`
    should implement the abstruct method
    :meth:`~PipelineProperty.provide_value`, which accept an argument, the
    instance of :class:`~brownant.dinergate.Dinergate`.

    Overriding :meth:`~brownant.pipeline.base.PipelineProperty.prepare` is
    optional in subclasses.

    :param kwargs: the parameters with the three kinds.
    """

    #: the names of required attributes.
    required_attrs = set()

    def __init__(self, **kwargs):
        super(PipelineProperty, self).__init__(self.provide_value)
        self.__name__ = None
        self.__module__ = None
        self.__doc__ = None

        #: the definition of attr_names
        self.attr_names = {}
        #: the definition of options
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
        missing_attrs = self.required_attrs - assigned_attrs
        if missing_attrs:
            raise TypeError("missing %r" % ", ".join(missing_attrs))

        self.prepare()

    def prepare(self):
        """This method will be called after instance ininialized. The
        subclasses could override the implementation.

        In general purpose, the implementation of this method should give
        default value to options and the members of
        :attr:`~brownant.pipeline.base.PipelineProperty.attr_names`.

        Example:

        .. code-block:: python

           def prepare(self):
               self.attr_names.setdefault("text_attr", "text")
               self.options.setdefault("use_proxy", False)
        """

    def get_attr(self, obj, name):
        """Get attribute of the target object with the configured attribute
        name in the :attr:`~brownant.pipeline.base.PipelineProperty.attr_names`
        of this instance.

        :param obj: the target object.
        :type obj: :class:`~brownant.dinergate.Dinergate`
        :param name: the internal name used in the
                :attr:`~brownant.pipeline.base.PipelineProperty.attr_names`.
                (.e.g. `"text_attr"`)
        """
        attr_name = self.attr_names[name]
        return getattr(obj, attr_name)
