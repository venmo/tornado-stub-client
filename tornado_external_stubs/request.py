class StubbedRequest(object):

    def __init__(self, method_name, path):
        self.method_name = method_name.lower()
        self.path = path

    def matches(self, other_stubbed_request):
        return self.method_name == other_stubbed_request.method_name \
                and self.path == other_stubbed_request.path

class StubbedRequestWithResponse(object):

    def __init__(self, request, return_body):
        self.request = request
        self.return_body = return_body
