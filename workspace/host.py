from client.httpclient import DefaultHttpClient
from client.resourceclient import AuthenticationClient
from client.resourceclient import AirlockSession
from client.resourceclient import ConfigurationClient


class Host:
    def __init__(self, host_name: str, token: str):
        self.auth_client = AuthenticationClient(http_client=DefaultHttpClient(host_name), token=token)
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


class ResourceObject:
    def attributes(self) -> str:
        raise Exception()

    def id(self) -> str:
        raise Exception()

    def type(self) -> str:
        raise Exception()
