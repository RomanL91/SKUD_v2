from threading import current_thread

from django.utils.deprecation import MiddlewareMixin

from multiprocessing import Process, Queue


class MultiprocessingDecorator:
    # TO DO возрашать ошибку в админку

    def __call__(self, func):
        q = Queue()
        def wrapper(*args, **kwargs):
            print('ВЫЗОВ wrapper')
            def subprocess():
                q.put(func(*args, **kwargs))
            p = Process(target=subprocess)
            p.start()
        return wrapper
    

class MessagesMiddleware: 
    def __init__(self, get_response): 
        self.get_response = get_response 

    def __call__(self, request): 
        response = self.get_response(request) 
        return response 
    

# не используется
_requests = {}
def current_request():
    return _requests.get(current_thread().ident, None)


# не используется
class RequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        _requests[current_thread().ident] = request

    def process_response(self, request, response):
        # when response is ready, request should be flushed
        _requests.pop(current_thread().ident, None)
        return response


    def process_exception(self, request, exception):
        # if an exception has happened, request should be flushed too
         _requests.pop(current_thread().ident, None)
    