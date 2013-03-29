from collections import defaultdict
from urlparse import urlparse

def _new_collection():
    """ Collection data type is
            {path: {method: (ResponseClass,) }}
        So e.g. a POST request to http://venmo.com/feed is stored as
        {'/feed': {'POST': (ResponseClass,)}}

        the ResponseClass will have had the the constructor partially applied
        with the specified stubbed data so after finding it we finish
        instantiatiing with the request we received and return it.
        Why? So the request attribute on the response is the request that
        was made, not just the matching criteria in the stub
    """
    return defaultdict(lambda: defaultdict(lambda: ()))

class RequestCollection(object):

    _requests = _new_collection()

    @classmethod
    def add(cls, request, response):
        parsed = urlparse(request.url)
        cls._requests[parsed.path][request.method] = \
                cls._requests[parsed.path][request.method] + (response,)

    @classmethod
    def find(cls, request):
        parsed = urlparse(request.url)
        head = cls._requests[parsed.path][request.method][0]
        cls._requests[parsed.path][request.method] = \
                cls._requests[parsed.path][request.method][1:] + (head,)
        return head

    @classmethod
    def remove(cls, request):
        parsed = urlparse(request.url)
        del cls._requests[parsed.path][request.method]

    @classmethod
    def reset(cls):
        cls._requests = _new_collection()
