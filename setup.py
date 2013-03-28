from distutils.core import setup
setup(
    name="tornado-stub-client",
    description="Stubs out tornado AsyncHTTPClient.fetch with a nice interface, for testing code that relies on async code",
    version='0.1',
    packages=["tornado_stub_client"],
)
