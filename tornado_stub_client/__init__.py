from .httpclient import AsyncStubHTTPClient
from .collection import RequestCollection
from .commands import stub

# see http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
import pkg_resources
VERSION = pkg_resources.require('tornado_stub_client')[0].version
del pkg_resources

def reset():
    RequestCollection.reset()
