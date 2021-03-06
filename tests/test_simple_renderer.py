import asyncio
import socket
import unittest
import aiohttp
from aiohttp import web
from aiohttp.multidict import CIMultiDict
import aiohttp_jinja2
import jinja2
from unittest import mock


class TestSimple(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def find_unused_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def make_request(self, app, method, path):
        headers = CIMultiDict()
        message = aiohttp.RawRequestMessage(method, path,
                                            aiohttp.HttpVersion(1, 1),
                                            headers, False, False)
        self.payload = mock.Mock()
        self.transport = mock.Mock()
        self.writer = mock.Mock()
        req = web.Request(app, message, self.payload,
                          self.transport, self.writer, 15)
        return req

    def test_func(self):

        @aiohttp_jinja2.template('tmpl.jinja2')
        @asyncio.coroutine
        def func(request):
            return {'head': 'HEAD', 'text': 'text'}

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            aiohttp_jinja2.setup(app, loader=jinja2.DictLoader(
                {'tmpl.jinja2':
                 "<html><body><h1>{{head}}</h1>{{text}}</body></html>"}))

            app.router.add_route('GET', '/', func)

            port = self.find_unused_port()
            srv = yield from self.loop.create_server(
                app.make_handler(), '127.0.0.1', port)
            url = "http://127.0.0.1:{}/".format(port)

            resp = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(200, resp.status)
            txt = yield from resp.text()
            self.assertEqual('<html><body><h1>HEAD</h1>text</body></html>',
                             txt)

            srv.close()
            self.addCleanup(srv.close)

        self.loop.run_until_complete(go())

    def test_meth(self):

        class Handler:

            @aiohttp_jinja2.template('tmpl.jinja2')
            @asyncio.coroutine
            def meth(self, request):
                return {'head': 'HEAD', 'text': 'text'}

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            aiohttp_jinja2.setup(app, loader=jinja2.DictLoader(
                {'tmpl.jinja2':
                 "<html><body><h1>{{head}}</h1>{{text}}</body></html>"}))

            handler = Handler()
            app.router.add_route('GET', '/', handler.meth)

            port = self.find_unused_port()
            srv = yield from self.loop.create_server(
                app.make_handler(), '127.0.0.1', port)
            url = "http://127.0.0.1:{}/".format(port)

            resp = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(200, resp.status)
            txt = yield from resp.text()
            self.assertEqual('<html><body><h1>HEAD</h1>text</body></html>',
                             txt)

            srv.close()
            self.addCleanup(srv.close)

        self.loop.run_until_complete(go())

    def test_convert_func_to_coroutine(self):

        @aiohttp_jinja2.template('tmpl.jinja2')
        def func(request):
            return {'head': 'HEAD', 'text': 'text'}

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            aiohttp_jinja2.setup(app, loader=jinja2.DictLoader(
                {'tmpl.jinja2':
                 "<html><body><h1>{{head}}</h1>{{text}}</body></html>"}))

            app.router.add_route('GET', '/', func)

            port = self.find_unused_port()
            srv = yield from self.loop.create_server(
                app.make_handler(), '127.0.0.1', port)
            url = "http://127.0.0.1:{}/".format(port)

            resp = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(200, resp.status)
            txt = yield from resp.text()
            self.assertEqual('<html><body><h1>HEAD</h1>text</body></html>',
                             txt)

            srv.close()
            self.addCleanup(srv.close)

        self.loop.run_until_complete(go())

    def test_render_not_initialized(self):

        @asyncio.coroutine
        def func(request):
            return aiohttp_jinja2.render_template('template', request, {})

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)

            app.router.add_route('GET', '/', func)

            req = self.make_request(app, 'GET', '/')

            with self.assertRaises(web.HTTPInternalServerError) as ctx:
                yield from func(req)

            self.assertEqual("Template engine is not initialized, "
                             "call aiohttp_jinja2.setup(app_key={}) first"
                             "".format(aiohttp_jinja2.APP_KEY),
                             ctx.exception.text)

        self.loop.run_until_complete(go())

    def test_set_status(self):

        @aiohttp_jinja2.template('tmpl.jinja2', status=201)
        def func(request):
            return {'head': 'HEAD', 'text': 'text'}

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            aiohttp_jinja2.setup(app, loader=jinja2.DictLoader(
                {'tmpl.jinja2':
                 "<html><body><h1>{{head}}</h1>{{text}}</body></html>"}))

            app.router.add_route('GET', '/', func)

            port = self.find_unused_port()
            srv = yield from self.loop.create_server(
                app.make_handler(), '127.0.0.1', port)
            url = "http://127.0.0.1:{}/".format(port)

            resp = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(201, resp.status)
            txt = yield from resp.text()
            self.assertEqual('<html><body><h1>HEAD</h1>text</body></html>',
                             txt)

            srv.close()
            self.addCleanup(srv.close)

        self.loop.run_until_complete(go())

    def test_render_template(self):

        @asyncio.coroutine
        def func(request):
            return aiohttp_jinja2.render_template(
                'tmpl.jinja2', request,
                {'head': 'HEAD', 'text': 'text'})

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            aiohttp_jinja2.setup(app, loader=jinja2.DictLoader(
                {'tmpl.jinja2':
                 "<html><body><h1>{{head}}</h1>{{text}}</body></html>"}))

            app.router.add_route('GET', '/', func)

            port = self.find_unused_port()
            srv = yield from self.loop.create_server(
                app.make_handler(), '127.0.0.1', port)
            url = "http://127.0.0.1:{}/".format(port)

            resp = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(200, resp.status)
            txt = yield from resp.text()
            self.assertEqual('<html><body><h1>HEAD</h1>text</body></html>',
                             txt)

            srv.close()
            self.addCleanup(srv.close)

        self.loop.run_until_complete(go())

    def test_template_not_found(self):

        @asyncio.coroutine
        def func(request):
            return aiohttp_jinja2.render_template('template', request, {})

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            aiohttp_jinja2.setup(app, loader=jinja2.DictLoader({}))

            app.router.add_route('GET', '/', func)

            req = self.make_request(app, 'GET', '/')

            with self.assertRaises(web.HTTPInternalServerError) as ctx:
                yield from func(req)

            self.assertEqual("Template 'template' not found",
                             ctx.exception.text)

        self.loop.run_until_complete(go())

    def test_render_not_mapping(self):

        @aiohttp_jinja2.template('tmpl.jinja2')
        @asyncio.coroutine
        def func(request):
            return 123

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            aiohttp_jinja2.setup(app, loader=jinja2.DictLoader(
                {'tmpl.jinja2': "tmlp"}))

            app.router.add_route('GET', '/', func)

            req = self.make_request(app, 'GET', '/')

            with self.assertRaises(web.HTTPInternalServerError) as ctx:
                yield from func(req)

            self.assertEqual("context should be mapping, not <class 'int'>",
                             ctx.exception.text)

        self.loop.run_until_complete(go())

    def test_get_env(self):

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            aiohttp_jinja2.setup(app, loader=jinja2.DictLoader(
                {'tmpl.jinja2': "tmlp"}))

            env = aiohttp_jinja2.get_env(app)
            self.assertIsInstance(env, jinja2.Environment)
            self.assertIs(env, aiohttp_jinja2.get_env(app))

        self.loop.run_until_complete(go())
