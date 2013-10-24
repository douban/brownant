import lxml.html

from brownant.pipeline.base import PipelineProperty


class ElementTreeProperty(PipelineProperty):
    """The element tree built from a text response property. There is an usage
    example::

        class MySite(Dinergate):
            text_response = "<html></html>"
            div_response = "<div></div>"
            xml_response = (u"<?xml version='1.0' encoding='UTF-8'?>"
                            u"<result>\u6d4b\u8bd5</result>")
            etree = ElementTreeProperty()
            div_etree = ElementTreeProperty(text_response_attr="div_response")
            xml_etree = ElementTreeProperty(text_response_attr="xml_response",
                                            encoding="utf-8")

        site = MySite(request)
        print(site.etree)  # output: <Element html at 0x1f59350>
        print(site.div_etree)  # output: <Element div at 0x1f594d0>
        print(site.xml_etree)  # output: <Element result at 0x25b14b0>

    :param text_response_attr: optional. default: `"text_response"`.
    :param encoding: optional. default: `None`. The output text could be
                     encoded to a specific encoding.

    .. versionadded:: 0.1.4
       The `encoding` optional parameter.
    """

    def prepare(self):
        self.attr_names.setdefault("text_response_attr", "text_response")
        self.options.setdefault("encoding", None)

    def provide_value(self, obj):
        text_response = self.get_attr(obj, "text_response_attr")
        if self.options["encoding"]:
            text_response = text_response.encode(self.options["encoding"])
        return lxml.html.fromstring(text_response)


class XPathTextProperty(PipelineProperty):
    """The text extracted from a element tree property by XPath. There is an
    example for usage::

        class MySite(Dinergate):
            # omit page_etree
            title = XPathTextProperty(xpath=".//h1[@id='title']/text()",
                                      etree_attr="page_etree",
                                      strip_spaces=True,
                                      pick_mode="first")
            links = XPathTextProperty(xpath=".//*[@id='links']/a/@href",
                                      etree_attr="page_etree",
                                      strip_spaces=True,
                                      pick_mode="join",
                                      joiner="|")

    :param xpath: the xpath expression for extracting text.
    :param etree_attr: optional. default: `"etree"`.
    :param strip_spaces: optional. default: `False`. if it be `True`,
                         the spaces in the beginning and the end of texts will
                         be striped.
    :param pick_mode: optional. default: `"join"`, and could be "join", "first"
                      or "keep". while `"join"` be detected, the texts will be
                      joined to one. if the `"first"` be detected, only
                      the first text would be picked. if the `"keep"` be
                      detected, the original value will be picked.
    :param joiner: optional. default is a space string. it is no sense in
                   assigning this parameter while the `pick_mode` is not
                   `"join"`. otherwise, the texts will be joined by this
                   string.

    .. versionadded:: 0.1.4
       The new option value `"keep"` of the `pick_mode` parameter.
    """

    required_attrs = {"xpath"}

    def prepare(self):
        self.attr_names.setdefault("etree_attr", "etree")
        self.options.setdefault("strip_spaces", False)
        self.options.setdefault("pick_mode", "join")
        self.options.setdefault("joiner", " ")

    def choice_pick_impl(self):
        pick_mode = self.options["pick_mode"]
        impl = {
            "join": self.pick_joining,
            "first": self.pick_first,
            "keep": self.keep_value,
        }.get(pick_mode)

        if not impl:
            raise ValueError("%r is not valid pick mode" % pick_mode)
        return impl

    def pick_joining(self, value):
        joiner = self.options["joiner"]
        return joiner.join(value)

    def pick_first(self, value):
        return value[0] if value else ""

    def keep_value(self, value):
        return value

    def provide_value(self, obj):
        etree = self.get_attr(obj, "etree_attr")
        value = etree.xpath(self.xpath)
        pick_value = self.choice_pick_impl()

        if self.options["strip_spaces"]:
            value = [v.strip() for v in value if v.strip()]

        return pick_value(value)
