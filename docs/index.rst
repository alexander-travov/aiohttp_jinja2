.. aiohttp_jinja2 documentation master file, created by
   sphinx-quickstart on Sun Mar 22 12:04:15 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

aiohttp_jinja2
==============


.. currentmodule:: aiohttp_jinja2


jinja2_ template renderer for `aiohttp.web`__.


.. _jinja2: http://jinja.pocoo.org

.. _aiohttp_web: http://aiohttp.readthedocs.org/en/latest/web.html

__ aiohttp_web_


Usage
-----

Before template rendering you have to setup *jinja2 environment*
(:class:`jinja2.Environment`)first::

    app = web.Application(loop=self.loop)
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader('/path/to/templates/folder'))


After that you may use template engine in your
:term:`web-handlers<web-handler>`. The most convinient way is to
decorate :term:`web-handler`::

    @aiohttp_jinja2.template('tmpl.jinja2')
    def handler(request):
        return {'name': 'Andrew', 'surname': 'Svetlov'}

On handler call the :func:`template` decorator will pass
returned dictionary ``{'name': 'Andrew', 'surname': 'Svetlov'}`` into
template named ``"tmpl.jinja2"`` for getting resulting HTML text.

If you need more complex processing (set response headers for example)
you may call :func:`render_template` function::

    @asyncio.coroutine
    def handler(request):
        context = {'name': 'Andrew', 'surname': 'Svetlov'}
        response = aiohttp_jinja2.render_template('tmpl.jinja2',
                                                  request,
                                                  context)
        response.headers['Content-Language'] = 'ru'
        return response

.. _aiohttp_jinja2-reference:

Reference
---------

.. highlight:: python

.. module:: aiohttp_jinja2

.. currentmodule:: aiohttp_jinja2


.. data:: APP_KEY

   The key name in :class:`aiohttp.web.Application` dictionary,
   ``'aiohttp_jinja2_environment'`` for storing :term:`jinja2`
   environment object (:class:`jinja2.Environment`).

   Usually you don't need to operate with *application* manually, left
   it to :mod:`aiohttp_jinja2` functions.


.. function:: get_env(app, app_key=APP_KEY)

   Return :class:`jinja2.Environment` object which has stored in the
   *app* (:class:`aiohttp.web.Application` instance).

   *app_key* is an optional key for application dict, :const:`APP_KEY`
   by default.


.. function:: render_template(template_name, request, context, *, \
                              app_key=APP_KEY, encoding='utf-8')

   Return :class:`aiohttp.web.Response` which contains template
   *template_name* filled with *context* and is a response to
   *request* (:class:`aiohttp.web.Request` instance).

   *app_key* is an optional key for application dict, :const:`APP_KEY`
   by default.

   *encoding* is response encoding, ``'utf-8'`` by default.

   Returned response has *Content-Type* header set to ``'text/html'``.


.. decorator:: template(template_name, *, app_key=APP_KEY, encoding='utf-8',\
                        status=200)

   Decorate :term:`web-handler` to convert returned :class:`dict`
   context into :class:`aiohtttp.web.Response` filled with
   *template_name* template.

   *app_key* is an optional key for application dict, :const:`APP_KEY`
   by default.

   *encoding* is response encoding, ``'utf-8'`` by default.

   *status* is *HTTP status code* for returned response, *200* (OK) by
   default.

   Returned response has *Content-Type* header set to ``'text/html'``.


License
-------

:mod:`aiohttp_jinja2` is offered under the Apache 2 license.

Glossary
--------

.. if you add new entries, keep the alphabetical sorting!

.. glossary::

   jinja2

       A modern and designer-friendly templating language for Python.

       See http://jinja.pocoo.org/

   web-handler

       An enpoint that returns http response.


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`