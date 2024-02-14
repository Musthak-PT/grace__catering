import threading

_local = threading.local()

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the request in the thread-local variable
        _local.request = request

        response = self.get_response(request)

        return response

def get_current_request():
    # Retrieve the request from the thread-local variable
    return getattr(_local, 'request', None)
