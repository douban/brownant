from brownant.pipeline.base import PipelineProperty
from brownant.exceptions import NotSupported


class QueryArgument(PipelineProperty):

    required_attrs = {"name"}

    def prepare(self):
        self.attr_names.setdefault("request_attr", "request")
        self.options.setdefault("type", None)
        self.options.setdefault("required", True)

    def provide_value(self, obj):
        request = self.get_attr(obj, "request_attr")
        value = request.args.get(self.name, type=self.options["type"])
        if self.options["required"] and not value:
            raise NotSupported
        return value


class RawHtml(PipelineProperty):

    def prepare(self):
        self.attr_names.setdefault("url_attr", "url")
        self.attr_names.setdefault("http_client_attr", "http_client")

    def provide_value(self, obj):
        url = self.get_attr(obj, "url_attr")
        http_client = self.get_attr(obj, "http_client_attr")
        response = http_client.get(url)
        response.raise_for_status()
        return response.text
