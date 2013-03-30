# python 3 has different package names
try: from urlparse import urlparse
except ImportError: from urllib.parse import urlparse

from collections import defaultdict

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
        responses = cls._requests[parsed.path][request.method]
        if len(responses) > 0:
            head = responses[0]
            cls._requests[parsed.path][request.method] = \
                    cls._requests[parsed.path][request.method][1:] + (head,)
        else:
            head = None
        return head

    @classmethod
    def remove(cls, request):
        parsed = urlparse(request.url)
        del cls._requests[parsed.path][request.method]

    @classmethod
    def reset(cls):
        cls._requests = _new_collection()
