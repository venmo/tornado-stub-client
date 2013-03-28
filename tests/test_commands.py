from unittest import TestCase
import json

from tornado_stub_client import stub, reset
from tornado_stub_client.collection import RequestCollection

class CommandsTest(TestCase):
    """ the stub() command is actually a class who's initializer returns
    itself, so we can do stub().and_return() in a ruby rspec mock fashion
    """

    def setUp(self):
        reset()

    def test_init_stub(self):
        s = stub("/hello")
        self.assertTrue(isinstance(s, stub))
        self.assertEqual(s.request.url, "/hello")

    def test_init_add_and_return(self):
        st = stub("/hello")
        req = st.request
        st = st.and_return(body="foobar body")
        response = st.response_partial(req, 200)
        self.assertEquals(response.code, 200)
        self.assertEquals(response.body, "foobar body")
        self.assertEquals(response.request.url, "/hello")

    def test_init_stub_creates_blank_response_partial(self):
        st = stub("/hello")
        response = st.response_partial(st.request, 200)
        self.assertEquals(response.code, 200)
        self.assertEquals(response.body, None)

    def test_stub_with_method(self):
        st = stub("/hello", method="POST").and_return(body="anything")
        resp_partial = RequestCollection.find(st.request)
        self.assertNotEqual(resp_partial, None)

    def test_return_with_body_json(self):
        st = stub("/hello").and_return(body_json={'name': 'somebody'})
        resp_partial = RequestCollection.find(st.request)
        resp = resp_partial(st.request, 200)
        self.assertEqual(json.loads(resp.body).get('name'), 'somebody')

    def test_no_body(self):
        st = stub("/hello").and_return(body=None)
        resp_partial = RequestCollection.find(st.request)
        resp = resp_partial(st.request, 200)
        self.assertEqual(resp.body, '') 
