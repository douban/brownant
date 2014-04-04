.. _quickstart:

Quick Start
===========

There are some simple examples built with Brownant.


The Minimal Demo
----------------

This demo could get the download link from the PyPI home page of given
project.

.. code-block:: python

    # example.py
    from brownant import Brownant, Site
    from lxml import html
    from requests import Session

    site = Site(name="pypi")
    http = Session()


    @site.route("pypi.python.org", "/pypi/<name>", defaults={"version": None})
    @site.route("pypi.python.org", "/pypi/<name>/<version>")
    def pypi_info(request, name, version):
        url = request.url.geturl()
        etree = html.fromstring(http.get(url).content)
        download_url = etree.xpath(".//div[@id='download-button']/a/@href")[0]

        return {"name": name, "version": version, "download_url": download_url}

    app = Brownant()
    app.mount_site(site)

    if __name__ == "__main__":
        from pprint import pprint
        pprint(app.dispatch_url("https://pypi.python.org/pypi/Werkzeug/0.9.4"))

And run it, we will get the output::

    $ python example.py
    {'download_url': 'https://.../source/W/Werkzeug/Werkzeug-0.9.4.tar.gz',
     'name': u'Werkzeug',
     'version': u'0.9.4'}


The Declarative Demo
--------------------

With the declarative usage, the workflow will be flexible and readable.

First, we define the "dinergate" in a site supported module:

.. code-block:: python

    # sites/pypi.py
    from brownant.site import Site
    from brownant.dinergate import Dinergate
    from brownant.pipeline.network import TextResponseProperty
    from brownant.pipeline.html import ElementTreeProperty, XPathTextProperty

    site = Site(name="pypi")


    @site.route("pypi.python.org", "/pypi/<name>/<version>")
    class PythonPackageInfo(Dinergate):

        URL_TEMPLATE = "http://pypi.python.org/pypi/{self.name}/{self.version}"

        text_response = TextResponseProperty()
        etree = ElementTreeProperty()
        download_url = XPathTextProperty(
            xpath=".//div[@id='download-button']/a/@href",
            strip_spaces=True, pick_mode="first")

        @property
        def info(self):
            return {"name": self.name, "version": self.version,
                    "download_url": self.download_url}

And then we define an application instance and mount the site.

.. code-block:: python

    # app.py
    from brownant import Brownant

    app = Brownant()
    app.mount_site("sites.pypi:site")


    if __name__ == "__main__":
        from pprint import pprint
        pkg = app.dispatch_url("https://pypi.python.org/pypi/Werkzeug/0.9.4")
        pprint(pkg.info)

And run it, we will get the same output.
