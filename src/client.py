import requests


class HttpClient:
    def __init__(self, host_name):
        self.host_name = host_name
        self.session = requests.session()

    def get(self, path, headers={'Accept': 'application/json'}):
        return self.session.get(
            url=self.url(path),
            headers=headers,
            verify=False
        )

    def post(self, path, data=None, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}):
        return self.session.post(
            url=self.url(path),
            headers=headers,
            data=data,
            verify=False
        )

    def put(self, path, data=None, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}):
        return self.session.put(
            url=self.url(path),
            headers=headers,
            data=data,
            verify=False
        )

    def patch(self, path, data=None, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}):
        return self.session.patch(
            url=self.url(path),
            headers=headers,
            data=data,
            verify=False
        )

    def delete(self, path, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}):
        return self.session.delete(
            self.url(path),
            headers=headers,
            verify=False
        )

    def url(self, path):
        return f"{self.host_name}{path}"


class SessionClient:
    def __init__(self, http_client, token):
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
    def __init__(self, http_client):
        self.client = http_client

    def load_current_active_configuration(self):
        return self.client.post("/airlock/rest/configuration/configurations/load-active")

    def save(self, comment):
        return self.client.post(
            path="/airlock/rest/configuration/configurations/save",
            data=f"{{ \"comment\" : \"{comment}\" }}"
        )


class ResourceClient:
    def __init__(self, http_client, base_path):
        self.client = http_client
        self.base_path = base_path

    def all(self):
        return self.client.get(self.base_path)

    def get(self, id):
        return self.client.get(f"{self.base_path}/{id}")

    def create(self, data):
        return self.client.post(
            path=self.base_path,
            data=data
        )

    def update(self, id, data):
        return self.client.patch(
            path=f"{self.base_path}/{id}",
            data=data
        )

    def delete(self, id):
        return self.client.delete(f"{self.base_path}/{id}")

    def connect_to_resources(self, id, ref_id, ref_path, ref_type):
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

    def connect_to_resource(self, id, ref_id, ref_path, ref_type):
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
    def __init__(self, http_client):
        super().__init__(http_client, "/airlock/rest/configuration/nodes")


class OpenAPIClient(ResourceClient):
    def __init__(self, http_client):
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

    def connect_mapping(self, id, ref_id):
        return self.connect_to_resources(id, ref_id, "mappings", "mapping")


class SSLCertificateClient(ResourceClient):
    def __init__(self, http_client):
        super().__init__(http_client, "/airlock/rest/configuration/ssl-certificates")

    def connect_virtual_host(self, id, ref_id):
        return self.connect_to_resources(id, ref_id, "virtual-hosts", "virtual-host")


class VirtualHostClient(ResourceClient):
    def __init__(self, http_client):
        super().__init__(http_client, "/airlock/rest/configuration/virtual-hosts")

    def connect_ssl_certificate(self, id, ref_id):
        return self.connect_to_resource(id, ref_id, "ssl-certificate", "ssl-certificate")

    def connect_mapping(self, id, ref_id):
        return self.connect_to_resources(id, ref_id, "mappings", "mapping")


class MappingClient(ResourceClient):
    def __init__(self, http_client):
        super().__init__(http_client, "/airlock/rest/configuration/mappings")

    def connect_virtual_host(self, id, ref_id):
        return self.connect_to_resources(id, ref_id, "virtual-hosts", "virtual-host")

    def connect_back_end_group(self, id, ref_id):
        return self.connect_to_resource(id, ref_id, "back-end-group", "back-end-group")


class BackendGroupClient(ResourceClient):
    def __init__(self, http_client):
        super().__init__(http_client, "/airlock/rest/configuration/back-end-groups")

    def connect_mapping(self, id, ref_id):
        return self.connect_to_resources(id, ref_id, "mappings", "mapping")
