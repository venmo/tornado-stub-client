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

    def test_stub_no_return_doesnt_add_to_collection(self):
        st = stub("/hello")
        self.assertNotEqual(st.request, None)
        resp_partial = RequestCollection.find(st.request)
        self.assertEqual(resp_partial, None)

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

    def test_no_return_args(self):
        st = stub("/hello").and_return()
        resp_partial = RequestCollection.find(st.request)
        resp = resp_partial(st.request, 200)
        self.assertEqual(resp.body, '') 

    # def test_set_response_code_in_stub(self):
    #     st = stub("/hello").and_return(code=201)
    #     resp_partial = RequestCollection.find(st.request)
    #     resp = resp_partial(st.request)
    #     self.assertEqual(resp.code, 201)
