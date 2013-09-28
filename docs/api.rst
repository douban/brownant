.. _api:

Basic API
=========

The basic API included the application framework and routing system (provided
by :mod:`werkzeug.routing`) of brownant.

brownant.app
------------

.. autoclass:: brownant.app.BrownAnt
   :members:
   :inherited-members:

brownant.request
----------------

.. autoclass:: brownant.request.Request
   :members:
   :inherited-members:

brownant.site
-------------

.. autoclass:: brownant.site.Site
   :members:
   :inherited-members:


Declarative API
===============

The declarative API is around the "dinergate" and "pipeline property".

brownant.dinergate
------------------

.. autoclass:: brownant.dinergate.Dinergate
   :members:
   :inherited-members:

.. autoclass:: brownant.dinergate.DinergateType
   :show-inheritance:

brownant.pipeline.base
----------------------

.. autoclass:: brownant.pipeline.base.PipelineProperty
   :members:
   :inherited-members:
   :show-inheritance:

brownant.pipeline.network
-------------------------

.. autoclass:: brownant.pipeline.network.URLQueryProperty
   :members:

.. autoclass:: brownant.pipeline.network.TextResponseProperty
   :members:

brownant.pipeline.html
----------------------

.. autoclass:: brownant.pipeline.html.ElementTreeProperty
   :members:

.. autoclass:: brownant.pipeline.html.XPathTextProperty
   :members:
