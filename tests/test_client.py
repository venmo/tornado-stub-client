from unittest import TestCase
import functools
from cStringIO import StringIO
from tornado.testing import AsyncTestCase
from tornado.httpclient import HTTPRequest, HTTPResponse

from tornado_stub_client.collection import RequestCollection
from tornado_stub_client.httpclient import AsyncHTTPStubClient

class ClientTest(AsyncTestCase, TestCase):

    def setUp(self):
        super(ClientTest, self).setUp()
        RequestCollection.reset()

    def test_add_then_fetch(self):
        req = HTTPRequest("/hello")
        resp_partial = functools.partial(HTTPResponse,
                buffer=StringIO("response value"))
        RequestCollection.add(req, resp_partial)
        client = AsyncHTTPStubClient()
        client.fetch(req, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "response value")

    def test_fetch_string_converts_to_request_object(self):
        req = HTTPRequest("/hello")
        resp_partial = functools.partial(HTTPResponse,
                buffer=StringIO("response value"))
        RequestCollection.add(req, resp_partial)
        client = AsyncHTTPStubClient()
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "response value")

    def test_fetch_wrong_thing_returns_404(self):
        client = AsyncHTTPStubClient()
        client.fetch("/nothingasdfads", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)
        self.assertEqual(response.body, None)

    def test_post_and_git_are_different(self):
        req = HTTPRequest("/hello")
        resp_partial = functools.partial(HTTPResponse,
                buffer=StringIO("response value"))
        RequestCollection.add(req, resp_partial)

        AsyncHTTPStubClient().fetch("/hello", self.stop, method="POST")
        response = self.wait()
        self.assertEqual(response.code, 404)
