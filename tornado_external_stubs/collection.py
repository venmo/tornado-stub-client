from collections import defaultdict
from urlparse import urlparse

def _new_collection():
    return defaultdict(lambda: defaultdict(lambda: None))

class RequestCollection(object):

    _requests = _new_collection()

    @classmethod
    def add(cls, request, response):
        parsed = urlparse(request.url)
        cls._requests[parsed.path][request.method] = response

    @classmethod
    def find(cls, request):
        parsed = urlparse(request.url)
        return cls._requests[parsed.path][request.method]

    @classmethod
    def reset(cls):
        cls._requests = _new_collection()
