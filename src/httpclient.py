import requests
from .requestlogger import RequestLogger
from typing import Final


class HttpClient:
    DEFAULT_HEADERS: Final = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    """Default HTTP header"""

    def get(self, path: str, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """Sends a GET request

        :param path: URL path
        :param headers: HTTP headers
        :return: HTTP response
        """
        pass

    def post(self, path: str, data=None, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """Sends a POST request.

        Args:
            path (str): URL path
            data (str): HTTP body
            headers (dic): HTTP headers

        Returns
            requests.Response: HTTP response
        """
        pass

    def put(self, path: str, data=None, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """
        Sends a PUT request

        :param path: URL path
        :param data: HTTP body
        :param headers: HTTP headers
        :return: HTTP response
        """
        pass

    def patch(self, path: str, data=None, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """
        Sends a PATCH request

        :param path: URL path
        :param data: HTTP body
        :param headers: HTTP headers
        :return: HTTP Response
        """
        pass

    def delete(self, path: str, headers: dict = DEFAULT_HEADERS) -> type(requests.Response):
        """
        Sends a DELETE request

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
