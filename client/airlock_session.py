from .http_client import HttpClient
from requests import Response

class AirlockSession(HttpClient):
    def __init__(self, client: type(HttpClient)):
        self.client = client

    def get(self, path: str, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(Response):
        return self.client.get(path, headers)

    def post(self, path: str, data=None, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(Response):
        return self.client.post(path, data, headers)

    def put(self, path: str, data=None, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(Response):
        return self.client.put(path, data, headers)

    def patch(self, path: str, data=None, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(Response):
        return self.client.patch(path, data, headers)

    def delete(self, path, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(Response):
        return self.client.delete(path, headers)

    def terminate(self):
        return self.post(path="/airlock/rest/session/terminate")