import lxml.html

from brownant.pipeline.base import PipelineProperty


class ElementTree(PipelineProperty):

    def prepare(self):
        self.attr_names.setdefault("raw_html_attr", "raw_html")

    def provide_value(self, obj):
        raw_html = self.get_attr(obj, "raw_html_attr")
        return lxml.html.fromstring(raw_html)


class XPathText(PipelineProperty):

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
