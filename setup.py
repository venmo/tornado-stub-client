from distutils.core import setup
setup(
    name="tornado-stub-client",
    version="0.1",
    author="Danny Cosson",
    author_email="support@venmo.com",
    license="MIT",
    description="Stubs out tornado AsyncHTTPClient.fetch with a nice interface, for testing code that relies on async code",
    long_description=open("README.md").read(),
    url="https://github.com/venmo/tornado-stub-client",
    packages=["tornado_stub_client"],
    install_requires=[
        "tornado>=2.0",
    ],
)
