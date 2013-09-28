.. _userguide:

Quick Start
===========

There is a simple crawling application written with brownant. It could get
the download link from the PyPI home page of given project::

    from brownant.app import BrownAnt
    from brownant.site import Site
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

        return {
            "name": name,
            "version": version,
            "download_url": download_url,
        }

    app = BrownAnt()
    app.mount_site(site)

    if __name__ == "__main__":
        from pprint import pprint
        pprint(app.dispatch_url("https://pypi.python.org/pypi/Werkzeug/0.9.4"))

And run it, we will get the output::

    $ python example.py
    {'download_url': 'https://.../source/W/Werkzeug/Werkzeug-0.9.4.tar.gz',
     'name': u'Werkzeug',
     'version': u'0.9.4'}
