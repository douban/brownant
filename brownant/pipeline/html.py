import lxml.html

from brownant.pipeline.base import PipelineProperty


class ElementTreeProperty(PipelineProperty):
    """The element tree built from a text response property. There is an usage
    example::

        class MySite(Dinergate):
            text_response = "<html></html>"
            div_response = "<div></div>"
            etree = ElementTreeProperty()
            div_etree = ElementTreeProperty(text_response_attr="div_response")

        site = MySite(request)
        print(site.etree)  # output: <Element html at 0x1f59350>
        print(site.div_etree)  # output: <Element div at 0x1f594d0>

    :param text_response_attr: optional. default: `"text_response"`.
    """

    def prepare(self):
        self.attr_names.setdefault("text_response_attr", "text_response")

    def provide_value(self, obj):
        text_response = self.get_attr(obj, "text_response_attr")
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
    :param pick_mode: optional. default: `"join"`, and could be "join" or
                      "first". while `"join"` be detected, the texts will be
                      joined to one. otherwise the `"first"` be detected, only
                      the first text would be picked.
    :param joiner: optional. default is a space string. it is no sense in
                   assigning this parameter while the `pick_mode` is not
                   `"join"`. otherwise, the texts will be joined by this
                   string.
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
        }.get(pick_mode)

        if not impl:
            raise ValueError("%r is not valid pick mode" % pick_mode)
        return impl

    def pick_joining(self, value):
        joiner = self.options["joiner"]
        return joiner.join(value)

    def pick_first(self, value):
        return value[0] if value else ""

    def provide_value(self, obj):
        etree = self.get_attr(obj, "etree_attr")
        value = etree.xpath(self.xpath)
        pick_value = self.choice_pick_impl()

        if self.options["strip_spaces"]:
            value = [v.strip() for v in value if v.strip()]

        return pick_value(value)
