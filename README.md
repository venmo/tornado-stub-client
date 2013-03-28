## Tornado Stub Client

A library to make it easy to stub out async calls in tornado.  It stubs out AsyncHTTPClient.fetch, to be precise (but there's no need to be precise, that's the only asynchronous method in all of Tornado).  It works well but it's brand new, I have a couple more features to add.

Similar to [HTTParty](https://github.com/jnunemaker/httparty) but this just patches the `fetch()` method directly rather than the python socket.  Writing a new library was easier than trying to get HTTParty to work with the tornado async client.  If there's interest it would be easy enough to make this work with other http libs, e.g. requests or grequests, but you should probably just use HTTParty.

### Usage

```python
import tornado
from tornado_stub_client import stub, reset, AsyncStubHTTPClient

# For this example, SomeAsyncRestClient is a library in your codebase that
# wraps a REST api and maybe formats the results.
#
# Say it has a get_user() method that does a GET request to /user/:id (and
# takes a callback b/c it's async) and we want to stub it out

class MyAppTest(tornado.testing.AsyncTestCase):

    def test_one(self):
        myclient = SomeAsyncRestClient()
        myclient.http_client = AsyncStubHTTPClient() 
        with stub("http://api.example.com/user/10").and_return(
                body_json={'name': 'Danny Cosson',
                           'twitter_handle': '@dannycosson'}):
            myclient.get_user(10, self.stop())
            response_dict = self.wait()
            self.assertEquals(response_dict.get('name'), 'Danny Cosson')
```

See `tests/test_integration.py` for the working example code.  Note that you don't have to use `stub().and_return()` in a with statement, but if you don't that stub will stay there between tests so you should add a test suite setUp method that calls `reset()` to clear out the data.

### Tests

It would be strange to write an untested testing library.  To run the tests (probably in a virtualenv is best):

    $ cd tornado-stub-client
    $ python setup.py install
    $ pip install nose
    $ nosetests tests
