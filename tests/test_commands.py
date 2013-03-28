from unittest import TestCase

from tornado_stub_client.commands import stub


class CommandsTest(TestCase):
    """ the stub() command is actually a class who's initializer returns
    itself, so we can do stub().and_return() in a ruby rspec mock fashion
    """

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
