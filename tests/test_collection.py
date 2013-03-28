from unittest import TestCase
from tornado.httpclient import HTTPRequest

from tornado_external_stubs.collection import (RequestCollection,
                                               _new_collection)

class CollectionTest(TestCase):

    def setUp(self):
        RequestCollection._requests = _new_collection()

    def test_collection_two_levels(self):
        coll = _new_collection()
        try:
            coll["jklasdfkl"]["SOME_METHOD"]
        except KeyError:
            self.fail("RequestCollection not found should return None")

    def test_add(self):
        req = HTTPRequest("/hello")
        RequestCollection.add(req, "response val")
        val = RequestCollection._requests["/hello"]["GET"]
        self.assertEqual(val, "response val")

    def test_add_with_absolute_url(self):
        req = HTTPRequest("http://www.example.com:8000/hello")
        RequestCollection.add(req, "response val")
        val = RequestCollection._requests["/hello"]["GET"]
        self.assertEqual(val, "response val")

    def test_find_after_add(self):
        req = HTTPRequest("http://www.example.com:8000/hello")
        RequestCollection.add(req, "response val")
        val = RequestCollection.find(req)
        self.assertEqual(val, "response val")

    def test_reset(self):
        req = HTTPRequest("http://www.example.com:8000/hello")
        RequestCollection.add(req, "response val")
        RequestCollection.reset()
        self.assertEqual(len(RequestCollection._requests), 0)
