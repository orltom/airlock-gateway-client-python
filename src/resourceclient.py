from .httpclient import HttpClient


class ResourceClient:
    def __init__(self, http_client: type(HttpClient), base_path: str):
        self.client = http_client
        self.base_path = base_path

    def get(self):
        return self.client.get(self.base_path)

    def update(self, data):
        return self.client.patch(
            path=self.base_path,
            data=data
        )


class ResourceCRUDClient:
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

    def disconnect_to_resources(self, id: str, ref_id: str, ref_path: str, ref_type: str):
        return self.client.delete(
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

    def disconnect_to_resource(self, id: str, ref_id: str, ref_path: str, ref_type: str):
        return self.client.delete(
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


class AuthenticationClient:
    def __init__(self, token: str, http_client: type(HttpClient)):
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

    def all(self):
        return self.client.get(self.base_path)

    def save(self, comment: str):
        return self.client.post(
            path="/airlock/rest/configuration/configurations/save",
            data=f"{{ \"comment\" : \"{comment}\" }}"
        )

    def activate(self, comment: str):
        return self.client.post(
            path="/airlock/rest/configuration/configurations/activate",
            data=f"{{ \"comment\" : \"{comment}\" }}"
        )

    def load(self, id: str):
        return self.client.post(f"{self.base_path}/{id}")

    def load_current_active(self):
        return self.client.post("/airlock/rest/configuration/configurations/load-active")

    def export(self, id: str):
        return self.client.get(
            path=f"/airlock/rest/configuration/configurations/{id}/export",
            headers={"Accept": "application/zip"}
        )

    def export_current_loaded(self):
        return self.client.get(
            path="/airlock/rest/configuration/configurations/export",
            headers={"Accept": "application/zip"}
        )

    def import_config(self, data):
        return self.client.put(
            path="/airlock/rest/configuration/configurations/import",
            data=data,
            headers={"Content-Tyoe": "application/zip"}
        )


class VirtualHostClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/virtual-hosts")

    def connect_ssl_certificate(self, id: str, ref_id: str):
        return self.connect_to_resource(id, ref_id, "ssl-certificate", "ssl-certificate")

    def connect_mapping(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings", "mapping")

    def disconnect_ssl_certificate(self, id: str, ref_id: str):
        return self.disconnect_to_resource(id, ref_id, "ssl-certificate", "ssl-certificate")

    def disconnect_mapping(self, id: str, ref_id: str):
        return self.disconnect_to_resources(id, ref_id, "mappings", "mapping")


class MappingClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/mappings")

    def connect_virtual_host(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "virtual-hosts", "virtual-host")

    def connect_back_end_group(self, id: str, ref_id: str):
        return self.connect_to_resource(id, ref_id, "back-end-group", "back-end-group")

    def connect_open_api(self, id: str, ref_id: str):
        return self.connect_to_resource(id, ref_id, "openapi-document", "openapi-document")

    def disconnect_virtual_host(self, id: str, ref_id: str):
        return self.disconnect_to_resources(id, ref_id, "virtual-hosts", "virtual-host")

    def disconnect_back_end_group(self, id: str, ref_id: str):
        return self.disconnect_to_resource(id, ref_id, "back-end-group", "back-end-group")


class BackendGroupClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/back-end-groups")

    def connect_mapping(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings", "mapping")

    def disconnect_mapping(self, id: str, ref_id: str):
        return self.disconnect_to_resources(id, ref_id, "mappings", "mapping")


class SSLCertificateClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/ssl-certificates")

    def connect_virtual_host(self, id, ref_id):
        return self.connect_to_resources(id, ref_id, "virtual-hosts", "virtual-host")

    def disconnect_virtual_host(self, id, ref_id):
        return self.disconnect_to_resources(id, ref_id, "virtual-hosts", "virtual-host")


class OpenAPIClient(ResourceCRUDClient):
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

    def disconnect_mapping(self, id: str, ref_id: str):
        return self.disconnect_to_resources(id, ref_id, "mappings", "mapping")


class IPAddressList(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/ip-address-lists")

    def connect_mapping_whitelist(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings-whitelist", "mapping")

    def connect_mapping_blacklist(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings-blacklist", "mapping")

    def connect_mapping_blacklist_exception(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings-blacklist-exception", "mapping")

    def connect_mapping_request_frequency_filter(self, id: str, ref_id: str):
        return self.connect_to_resources(id, ref_id, "mappings-request-frequency-filter-whitelist", "mapping")


def disconnect_mapping_whitelist(self, id: str, ref_id: str):
    return self.disconnect_to_resources(id, ref_id, "mappings-whitelist", "mapping")


def disconnect_mapping_blacklist(self, id: str, ref_id: str):
    return self.disconnect_to_resources(id, ref_id, "mappings-blacklist", "mapping")


def disconnect_mapping_blacklist_exception(self, id: str, ref_id: str):
    return self.disconnect_to_resources(id, ref_id, "mappings-blacklist-exception", "mapping")


def disconnect_mapping_request_frequency_filter(self, id: str, ref_id: str):
    return self.disconnect_to_resources(id, ref_id, "mappings-request-frequency-filter-whitelist", "mapping")


class DynamicIPAddressBlackList(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/session")


class LicenseClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/log")


class NodeClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/nodes")


class DefaultGatewayClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/routes/default")


class RouteIPv4Client(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/routes/ipv4/source")


class RouteIPv6Client(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/routes/ipv6/source")


class HostClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/hosts")


class NetworkServiceClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/network-service")


class ICAPEnvironmentClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/icap-environments")


class KerberosEnvironmentClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/kerberos-environments")

    def connect_back_end_group(self, id: str, ref_id: str):
        return super().connect_to_resources(id, ref_id, "back-end-groups", "back-end-group")

    def disconnect_back_end_group(self, id: str, ref_id: str):
        return super().disconnect_to_resources(id, ref_id, "back-end-groups", "back-end-group")


class AllowedNetworkEnvironmentClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/allowed-network-endpoints")


class APIPolicyServiceClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/api-policy-services")

    def connect_mapping(self, id: str, ref_id: str):
        return super().connect_to_resources(id, ref_id, "mappings", "mapping")

    def disconnect_mapping(self, id: str, ref_id: str):
        return super().disconnect_to_resources(id, ref_id, "mappings", "mapping")


class LogSettingsClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/license")


class ReportingSettingsClient(ResourceClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/reporting")


class ValidatorMessageClient(ResourceCRUDClient):
    def __init__(self, http_client: type(HttpClient)):
        super().__init__(http_client, "/airlock/rest/configuration/validator-messages")
