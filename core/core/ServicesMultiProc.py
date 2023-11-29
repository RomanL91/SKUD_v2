from multiprocessing import Process, Queue

class MultiprocessingDecorator:
    # TO DO возрашать ошибку в админку

    # def __init__(self, target_func):
    #     self.pinger_func = target_func

    def __call__(self, func):
        q = Queue()
        def wrapper(*args, **kwargs):
            def subprocess():
                q.put(func(*args, **kwargs))
            p = Process(target=subprocess)
            p.start()
        return wrapper
