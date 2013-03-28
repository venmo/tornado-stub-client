# work with python 2.5, doesn't break in newer versions
from __future__ import with_statement
from unittest import TestCase
from tornado.testing import AsyncTestCase

from tornado_stub_client import stub, reset, AsyncStubHTTPClient

class IntegrationTest(AsyncTestCase, TestCase):

    def setUp(self):
        super(IntegrationTest, self).setUp()
        reset()

    def test_stub_and_fetch(self):
        client = AsyncStubHTTPClient()
        stub("/hello").and_return(body="world")
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "world")

    def test_can_fetch_twice(self):
        client = AsyncStubHTTPClient()
        stub("/hello").and_return(body="world")
        client.fetch("/hello", self.stop)
        self.wait()
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "world")

    def test_with_syntax(self):
        client = AsyncStubHTTPClient()
        with stub("/hello").and_return(body="world"):
            client.fetch("/hello", self.stop)
            response = self.wait()
            self.assertEqual(response.code, 200)
            self.assertEqual(response.body, "world")
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)
