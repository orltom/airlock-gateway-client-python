from client.http_client import DefaultHttpClient
from client.resource_client import AuthenticationClient
from client.resource_client import AirlockSession
from client.resource_client import ConfigurationClient


class Host:
    def __init__(self, host_name: str, token: str):
        http_client = DefaultHttpClient(host_name)
        self.auth_client = AuthenticationClient(http_client=http_client, token=token)
        self.session = None

    def configurations(self):
        self.session = self.auth_client.create()
        return ConfigurationHistory(self.session)


class ConfigurationHistory:
    def __init__(self, session: AirlockSession):
        self.session = session

    def load_current_active(self):
        configuration_client = ConfigurationClient(self.session)
        configuration_client.load_current_active()


class Workspace:
    def __init__(self, session: AirlockSession):
        self.session = session

    def mappings(self):
        raise Exception()

    def save(self, comment: str = ""):
        client = ConfigurationClient(self.session)
        client.save(comment)

    def activate(self, comment: str = ""):
        client = ConfigurationClient(self.session)
        client.activate(comment)


class Mappings:
    def all(self):
        raise Exception

    def find(self):
        raise Exception

    def add(self):
        raise Exception


class ResourceObject:
    def attributes(self) -> str:
        raise Exception()

    def id(self) -> str:
        raise Exception()

    def type(self) -> str:
        raise Exception()
