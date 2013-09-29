from brownant.pipeline.base import PipelineProperty
from brownant.exceptions import NotSupported


class URLQueryProperty(PipelineProperty):
    """The query argument property. The usage is simple::

        class MySite(Dinergate):
            item_id = URLQueryProperty(name="item_id", type=int)

    It equals to this::

        class MySite(Dinergate):
            @cached_property
            def item_id(self):
                value = self.request.args.get("item_id", type=int)
                if not value:
                    raise NotSupported
                return value

    A failure convertion with given type (:exc:`ValueError` be raised) will
    lead the value fallback to :obj:`None`. It is the same with the behavior of
    the :class:`~werkzeug.datastructures.MultiDict`.

    :param name: the query argument name.
    :param request_attr: optional. default: `"request"`.
    :param type: optionl. default: `None`. this value will be passed to
                 :meth:`~werkzeug.datastructures.MultiDict.get`.
    :param required: optionl. default: `True`. while this value be true, the
                     :exc:`~brownant.exceptions.NotSupported` will be raised
                     for meeting empty value.
    """

    required_attrs = {"name"}

    def prepare(self):
        self.attr_names.setdefault("request_attr", "request")
        self.options.setdefault("type", None)
        self.options.setdefault("required", True)

    def provide_value(self, obj):
        request = self.get_attr(obj, "request_attr")
        value = request.args.get(self.name, type=self.options["type"])
        if self.options["required"] and value is None:
            raise NotSupported
        return value


class TextResponseProperty(PipelineProperty):
    """The text response which returned by fetching network resource.

    Getting this property is network I/O operation in the first time. The
    http request implementations are all provided by :mod:`requests`.

    The usage example::

        class MySite(Dinergate):
            foo_http = requests.Session()
            foo_url = "http://example.com"
            foo_text = TextResponseProperty(url_attr="foo_url",
                                            http_client="foo_http",
                                            proxies=PROXIES)

    :param url_attr: optional. default: `"url"`. it point to the property which
                     could provide the fetched url.
    :param http_client_attr: optional. default: `"http_client"`. it point to
                             an http client property which is instance of
                             :class:`requests.Session`
    :param kwargs: the optional arguments which will be passed to
                   :meth:`requests.Session.get`.
    """

    def prepare(self):
        self.attr_names.setdefault("url_attr", "url")
        self.attr_names.setdefault("http_client_attr", "http_client")

    def provide_value(self, obj):
        url = self.get_attr(obj, "url_attr")
        http_client = self.get_attr(obj, "http_client_attr")
        response = http_client.get(url, **self.options)
        response.raise_for_status()
        return response.text
