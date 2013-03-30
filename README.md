## Tornado Stub Client

[![Build Status](https://travis-ci.org/venmo/tornado-stub-client.png?branch=master)](https://travis-ci.org/venmo/tornado-stub-client)

A library for stubbing async calls to external services in tornado.  It stubs out AsyncHTTPClient.fetch, to be precise (but there's no need to be precise, that's the only asynchronous method in all of Tornado).  It works well but it's brand new, I have a couple more features to add.

Similar to [HTTPretty](https://github.com/gabrielfalcao/HTTPretty) but this just patches the `fetch()` method directly rather than the python socket.  Writing a new library was easier than trying to get HTTPretty to work with the tornado async client.  If there's interest it would be easy enough to make this work with other http libs, e.g. requests or grequests, but you should probably just use HTTPretty.

### Usage

```python
import tornado
from tornado_stub_client import stub, reset, AsyncHTTPStubClient

class MyAppTest(tornado.testing.AsyncTestCase):

    def test_basic(self):
        client = AsyncHTTPStubClient()
        with stub("http://example.com").and_return(body="hello there"):
            client.fetch("http://example.com", self.stop)
            response = self.wait()
            self.assertEquals(response.code, 200)
            self.assertEquals(response.body, "hello there")
            
    def test_an_async_library(self):
        """ For this example, SomeRestLib is some async library that wraps a
        REST api. It has an AsyncHTTPClient as an instance variable.

        Let's say it has a method get_user(id, callback) that sends a GET to
        /user/:id and returns just json, and we want to unit test it
        """
        mylib = SomeRestLib()
        mylib.http_client = AsyncHTTPStubClient() 
        with stub("http://api.example.com/user/10").and_return(
                body_json={'name': 'Danny Cosson',
                           'twitter_handle': '@dannycosson'}):
            mylib.get_user(10, self.stop)
            response_dict = self.wait()
            self.assertEquals(response_dict.get('name'), 'Danny Cosson')

    def test_can_queue_stub_responses(self):
        """ A stub supports round-robin responses, i.e., a stub will cycle through
        queued responses. Handy for testing endpoints that handle state.
        """
        client = AsyncHTTPStubClient()
        with stub("/hello").and_return(body="hello")\
                           .and_return(body="world"):

            client.fetch("/hello", self.stop)
            response = self.wait()
            self.assertEqual(response.code, 200)
            self.assertEqual(response.body, "hello")

            client.fetch("/hello", self.stop)
            response = self.wait()
            self.assertEqual(response.code, 200)
            self.assertEqual(response.body, "world")
```

See `tests/test_integration.py` for working tests/example code.

Note that you don't have to use `stub().and_return()` in a `with` statement, but if you don't the stub you create won't get deleted between tests so you should add setUp or tearDown method that calls `reset()` to clear out the data.

### Tests

It would be strange to write an untested testing library.  To run the tests (probably in a virtualenv is best):

    $ cd tornado-stub-client
    $ pip install -r requirements.txt
    $ pip install nose
    $ nosetests tests
