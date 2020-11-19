import requests
from .requestlogger import RequestLogger
from typing import Final
from abc import ABCMeta


class HttpClient(metaclass=ABCMeta):
    """HTTP client which want implement HTTP request operation need to implement this interface."""

    DEFAULT_HEADERS: Final = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def get(self, path: str, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """Sends a HTTP GET request

        :param path: URL path
        :param headers: HTTP headers
        :return: HTTP response
        """
        pass

    def post(self, path: str, data=None, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """Sends a HTTP POST request.

        :param path: URL path
        :param data: HTTP body
        :param headers: HTTP headers
        :return: HTTP response
        """
        pass

    def put(self, path: str, data=None, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """
        Sends a HTTP PUT request

        :param path: URL path
        :param data: HTTP body
        :param headers: HTTP headers
        :return: HTTP response
        """
        pass

    def patch(self, path: str, data=None, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """
        Sends a HTTP PATCH request

        :param path: URL path
        :param data: HTTP body
        :param headers: HTTP headers
        :return: HTTP Response
        """
        pass

    def delete(self, path: str, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """
        Sends a HTTP DELETE request

        :param path: URL path
        :param headers: HTTP Headers
        :return: HTTP Response
        """
        pass


class DefaultHttpClient(HttpClient):

    def __init__(self, host_name: str):
        self.host_name = host_name
        self.session = requests.session()

    @RequestLogger
    def get(self, path: str, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(requests.Response):
        return self.session.get(
            url=self.url(path),
            headers=headers,
            verify=False
        )

    @RequestLogger
    def post(self, path: str, data=None, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(requests.Response):
        return self.session.post(
            url=self.url(path),
            headers=headers,
            data=data,
            verify=False
        )

    @RequestLogger
    def put(self, path: str, data=None, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(requests.Response):
        return self.session.put(
            url=self.url(path),
            headers=headers,
            data=data,
            verify=False
        )

    @RequestLogger
    def patch(self, path: str, data=None, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(requests.Response):
        return self.session.patch(
            url=self.url(path),
            headers=headers,
            data=data,
            verify=False
        )

    @RequestLogger
    def delete(self, path, headers: dict = HttpClient.DEFAULT_HEADERS) -> type(requests.Response):
        return self.session.delete(
            self.url(path),
            headers=headers,
            verify=False
        )

    def url(self, path: str) -> str:
        return f"{self.host_name}{path}"
