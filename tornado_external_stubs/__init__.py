from .httpclient import AsyncStubHTTPClient
from .collection import RequestCollection
from .commands import stub

def reset():
    RequestCollection.reset()
