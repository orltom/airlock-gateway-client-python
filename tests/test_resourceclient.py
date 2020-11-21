from client.httpclient import HttpClient
from client.resourceclient import AirlockSession
from requests import Response


class DummyHttpClient(HttpClient):
    def post(self, path: str, data=None, headers: dict = HttpClient.DEFAULT_HEADERS):
        response = Response()
        response.status_code = 200
        return response


def test_terminate():
    session = AirlockSession(DummyHttpClient())
    response = session.terminate()
    assert response.status_code == 200
