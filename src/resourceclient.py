from .httpclient import HttpClient


class SessionClient:
    def __init__(self, http_client: type(HttpClient), token: str):
        self.client = http_client
        self.token = token

    def create(self):
        return self.client.post(
            path="/airlock/rest/session/create",
            headers={
                'Authorization': f"Bearer {self.token}",
                'Accept': 'application/json'
            }
        )

    def terminate(self):
        return self.client.post("/airlock/rest/session/terminate")


class ConfigurationClient:
    def __init__(self, http_client: type(HttpClient)):
        self.client = http_client

    def load_current_active_configuration(self):
        return self.client.post("/airlock/rest/configuration/configurations/load-active")

    def save(self, comment: str):
        return self.client.post(
            path="/airlock/rest/configuration/configurations/save",
            data=f"{{ \"comment\" : \"{comment}\" }}"
        )


class ResourceClient:
    def __init__(self, http_client: type(HttpClient), base_path: str):
        self.client = http_client
        self.base_path = base_path

    def all(self):
        return self.client.get(self.base_path)

    def get(self, id: str):
        return self.client.get(f"{self.base_path}/{id}")

    def create(self, data):
        return self.client.post(
            path=self.base_path,
            data=data
        )

    def update(self, id: str, data):
        return self.client.patch(
            path=f"{self.base_path}/{id}",
            data=data
        )

    def delete(self, id: str):
        return self.client.delete(f"{self.base_path}/{id}")

    def connect_to_resources(self, id: str, ref_id: str, ref_path: str, ref_type: str):
        return self.client.patch(
            path=f"{self.base_path}/{id}/relationships/{ref_path}",
            data=(
                "{"
                "\"data\" : [{"
                f"\"type\" : \"{ref_type}\","
                f"\"id\" : \"{ref_id}\""
                "}]"
                "}"
            )
        )

    def connect_to_resource(self, id: str, ref_id: str, ref_path: str, ref_type: str):
        return self.client.patch(
            path=f"{self.base_path}/{id}/relationships/{ref_path}",
            data=(
                "{"
                "\"data\" : {"
                f"\"type\" : \"{ref_type}\","
                f"\"id\" : \"{ref_id}\""
                "}"
                "}"
            )
        )


class NodeClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/nodes")


class OpenAPIClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/api-security/openapi-documents")

    def upload(self, id, data):
        return self.client.patch(
            path=f"{self.base_path}/{id}",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/octet-stream'
            },
            data=data
        )

    def connect_mapping(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings", "mapping")


class SSLCertificateClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/ssl-certificates")

    def connect_virtual_host(self, id, ref_id):
        return self.connect_to_resources(id, ref_id, "virtual-hosts", "virtual-host")


class VirtualHostClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/virtual-hosts")

    def connect_ssl_certificate(self, id: str, ref_id: str):
        return self.connect_to_resource(id, ref_id, "ssl-certificate", "ssl-certificate")

    def connect_mapping(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings", "mapping")


class MappingClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/mappings")

    def connect_virtual_host(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "virtual-hosts", "virtual-host")

    def connect_back_end_group(self, id: str, ref_id: str):
        return self.connect_to_resource(id, ref_id, "back-end-group", "back-end-group")


class BackendGroupClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/back-end-groups")

    def connect_mapping(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings", "mapping")
