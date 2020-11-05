from time import time


class RequestLogger(object):

    def __init__(self, f):
        self.func = f

    def __call__(self, *args, **kwargs):
        start = time()
        resp = self.func(*args, **kwargs)
        duration = round((time() - start), 2)

        path = self.find_path(args, kwargs)
        headers = self.find_headers(args, kwargs)

        print(f"{self.func.__name__.upper()} {path} HTTP/1.1")
        for k, v in headers.items():
            print(k, ": ", v)
        print()
        print(f"Status Code: {resp.status_code} | Execution time: {duration}s")
        print("-" * 50)

        return resp

    def __get__(self, instance, owner):
        from functools import partial
        return partial(self.__call__, instance)

    def find_path(self, args, kwargs):
        if 'path' in kwargs:
            path = kwargs['path']
        else:
            path = args[1]
        return path

    def find_headers(self, args, kwargs):
        if 'headers' in kwargs:
            return kwargs['headers']
        elif len(args) >= 4:
            return args[3]
        else:
            return {}
