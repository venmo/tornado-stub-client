from unittest import TestCase
from tornado.testing import AsyncTestCase

from tornado_external_stubs import stub, reset, AsyncStubHTTPClient

class IntegrationTest(AsyncTestCase, TestCase):

    def setUp(self):
        super(IntegrationTest, self).setUp()
        reset()

    def test_example(self):
        client = AsyncStubHTTPClient()
        stub("/hello").and_return(body="world")
        client.fetch("/hello", self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "world")
