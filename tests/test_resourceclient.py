from client.http_client import HttpClient
from client.resource_client import AirlockSession, AuthenticationClient
from requests import Response
from pytest import raises


class DummyHttpClient(HttpClient):
    def __init__(self, status_code):
        self.status_code = status_code

    def post(self, path: str, data=None, headers: dict = HttpClient.DEFAULT_HEADERS):
        response = Response()
        response.status_code = self.status_code
        return response


def test_terminate():
    session = AirlockSession(DummyHttpClient(200))
    response = session.terminate()
    assert response.status_code == 200


def test_authentication_successful():
    authentication = AuthenticationClient("test", DummyHttpClient(200))
    airlock_session = authentication.create()
    assert type(airlock_session) == AirlockSession


def test_authentication_failed():
    authentication = AuthenticationClient("test", DummyHttpClient(500))
    with raises(Exception):
        authentication.create()
