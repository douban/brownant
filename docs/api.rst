.. _api:

Basic API
=========

The basic API included the application framework and routing system (provided
by :mod:`werkzeug.routing`) of Brownant.

brownant.app
------------

.. autoclass:: brownant.app.Brownant
   :members:
   :inherited-members:

.. autofunction:: brownant.app.redirect

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

brownant.exceptions
-------------------

.. autoexception:: brownant.exceptions.BrownantException

.. autoexception:: brownant.exceptions.NotSupported
   :show-inheritance:

brownant.utils
--------------

.. autofunction:: brownant.utils.to_bytes_safe

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

   .. method:: provide_value(obj)

      The abstruct method which should be implemented by subclasses. It provide
      the value expected by us from the subject instance.

      :param obj: the subject instance.
      :type obj: :class:`~brownant.dinergate.Dinergate`

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
