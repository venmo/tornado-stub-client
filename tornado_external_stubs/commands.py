import functools
from cStringIO import StringIO
from tornado.httpclient import HTTPRequest, HTTPResponse

from .collection import RequestCollection

class stub(object):

    def __init__(self, url):
        self.request = HTTPRequest(url)
        self.response_partial = HTTPResponse

    def and_return(self, body):
        """ When we get the response details in this call, we'll partially
        apply the HTTPResponse constructor, leaving out the status code and
        request object.  Those we'll fill in when fetching from the collection,
        just before returning to the user
        """
        self.response_partial = functools.partial(HTTPResponse,
                buffer=StringIO(body))
        RequestCollection.add(self.request, self.response_partial)
        return self
