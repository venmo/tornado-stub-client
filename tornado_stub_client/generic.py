from tornado import web

class GenericHandler(web.RequestHandler):

    method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def __init__(self, *args, **kwargs):
        super(GenericHandler, self).__init__(*args, **kwargs)
        for method in self.method_names:
            setattr(self, method, self.all_methods)

    def all_methods(self):
        if len(_queued_requests) == 0 :
            self.set_status(404)
            return
        expected_request = _queued_requests[0]
        request = StubbedRequest(self.request.method,
                                 self.request.path)
        if request.matches(expected_request):
            if expected_request.one_time:
                _queued_requests.pop(0)
            self.write(expected_request.return_body)
        else:
            self.set_status(404)

stubbed_app = web.Application([
    (r"^.*", GenericHandler),
])

class StubbedRequest(object):

    def __init__(self, method_name, path, return_body=None, one_time=False):
        self.method_name = method_name.lower()
        self.path = path
        self.return_body = return_body
        self.one_time = one_time

    def matches(self, other_stubbed_request):
        return self.method_name == other_stubbed_request.method_name \
            and self.path == other_stubbed_request.path

def register_uri(method_name, path, return_body, one_time=False):
    req = StubbedRequest(method_name, path, return_body, one_time)
    _queued_requests.append(req)

def reset():
    global _queued_requests
    _queued_requests = []

_queued_requests = [] 
