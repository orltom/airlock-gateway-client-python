from .http_client import HttpClient
from .airlock_session import AirlockSession
from .crud_client import ResourceCRUDClient, ResourceRUClient

class AuthenticationClient:
    def __init__(self, token: str, http_client: type(HttpClient)):
        self.client = http_client
        self.token = token

    def create(self):
        resp = self.client.post(
            path="/airlock/rest/session/create",
            headers={
                'Authorization': f"Bearer {self.token}",
                'Accept': 'application/json'
            }
        )
        if resp.status_code == 200:
            return AirlockSession(client=self.client)
        raise Exception("Authentication failed.")

class ConfigurationClient:
    def __init__(self, session: type(AirlockSession)):
        self.client = session

    def all(self):
        return self.client.get("/airlock/rest/configuration/configurations")

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

    def load(self, resource_id: str):
        return self.client.post(f"/airlock/rest/configuration/configurations/{resource_id}")

    def load_current_active(self):
        return self.client.post("/airlock/rest/configuration/configurations/load-active")

    def export(self, resource_id: str):
        return self.client.get(
            path=f"/airlock/rest/configuration/configurations/{resource_id}/export",
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
            headers={"Content-Type": "application/zip"}
        )


class SystemTemplateClient:
    def __init__(self, session: type(AirlockSession)):
        self.client = session

    def all(self):
        return self.client.get("/airlock/rest/configuration/templates/mappings")


class VirtualHostClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/virtual-hosts")

    def upload_crl(self, resource_id: str, data):
        return self.client.put(
            path=f"/configuration/virtual-hosts/{resource_id}/crl",
            headers={
                "Content-Type": "application/pkix-crl",
                "Accept": "application/json"
            },
            data=data
        )

    def delete_crl(self, resource_id: str, data):
        return self.client.delete(
            path=f"/configuration/virtual-hosts/{resource_id}/crl",
            headers={
                "Content-Type": "application/pkix-crl",
                "Accept": "application/json"
            },
            data=data
        )

    def connect_ssl_certificate(self, resource_id: str, ref_id: str):
        return self.connect_to_resource(resource_id, ref_id, "ssl-certificate")

    def connect_mapping(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "mapping")

    def disconnect_ssl_certificate(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resource(resource_id, ref_id, "ssl-certificate")

    def disconnect_mapping(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "mapping")


class MappingClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/mappings")

    def export(self, resource_id: str):
        return self.client.get(
            path=f"/configuration/mappings/{resource_id}/export",
            headers={"Accept": "application/zip"}
        )

    def import_as_new_or_replace(self, data):
        return self.client.put(
            path="/configuration/mappings/import",
            headers={
                "Content-Type": "application/zip",
                "Accept": "application/json"
            },
            data=data
        )

    def import_as_new_copy(self, data):
        return self.client.post(
            path="/configuration/mappings/import",
            headers={
                "Content-Type": "application/zip",
                "Accept": "application/json"
            },
            data=data
        )

    def apply_unlock_settings_from_source_mapping(self, resource_id: str):
        return self.client.post(
            path=f"/configuration/mappings/{resource_id}/pull-from-source-mapping",
        )

    def apply_unlock_settings_from_import(self, data):
        return self.client.post(
            path="/configuration/mappings/pull-from-uploaded-mappings",
            headers={
                "Content-Type": "application/zip",
                "Accept": "application/json"
            },
            data=data
        )

    def connect_virtual_host(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "virtual-host")

    def connect_back_end_group(self, resource_id: str, ref_id: str):
        return self.connect_to_resource(resource_id, ref_id, "back-end-group")

    def connect_open_api(self, resource_id: str, ref_id: str):
        return self.connect_to_resource(resource_id, ref_id, "openapi-document")

    def connect_ip_address_whitelist(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "ip-address-whitelist")

    def connect_ip_address_blacklist(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "ip-address-blacklist")

    def disconnect_virtual_host(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "virtual-host")

    def disconnect_back_end_group(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resource(resource_id, ref_id, "back-end-group")

    def disconnect_open_api(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resource(resource_id, ref_id, "openapi-document")

    def disconnect_ip_address_whitelist(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "ip-address-whitelist")

    def disconnect_ip_address_blacklist(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "ip-address-blacklist")


class BackendGroupClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/back-end-groups")

    def connect_mapping(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "mapping")

    def disconnect_mapping(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "mapping")


class SSLCertificateClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/ssl-certificates")

    def connect_virtual_host(self, resource_id, ref_id):
        return self.connect_to_resources(resource_id, ref_id, "virtual-host")

    def disconnect_virtual_host(self, resource_id, ref_id):
        return self.disconnect_to_resources(resource_id, ref_id, "virtual-host")


class OpenAPIClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/api-security/openapi-documents")

    def upload(self, resource_id, data):
        return self.client.patch(
            path=f"{self.base_path}/{resource_id}",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/octet-stream'
            },
            data=data
        )

    def connect_mapping(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "mapping")

    def disconnect_mapping(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "mapping")


class IPAddressList(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/ip-address-lists")

    def connect_mapping_whitelist(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "mappings-whitelist", "mapping")

    def connect_mapping_blacklist(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "mappings-blacklist", "mapping")

    def connect_mapping_blacklist_exception(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "mappings-blacklist-exception", "mapping")

    def connect_mapping_request_frequency_filter(self, resource_id: str, ref_id: str):
        return self.connect_to_resources(resource_id, ref_id, "mappings-request-frequency-filter-whitelist", "mapping")

    def disconnect_mapping_whitelist(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "mappings-whitelist", "mapping")

    def disconnect_mapping_blacklist(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "mappings-blacklist", "mapping")

    def disconnect_mapping_blacklist_exception(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "mappings-blacklist-exception", "mapping")

    def disconnect_mapping_request_frequency_filter(self, resource_id: str, ref_id: str):
        return self.disconnect_to_resources(resource_id, ref_id, "mappings-request-frequency-filter-whitelist","mapping")


class DynamicIPAddressBlackList(ResourceRUClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/session")


class LicenseClient(ResourceRUClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/license")


class NodeClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/nodes")


class DefaultGatewayClient(ResourceRUClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/routes/default")


class RouteIPv4Client(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/routes/ipv4/source")


class RouteIPv6Client(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/routes/ipv6/source")


class HostClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/hosts")


class NetworkServiceClient(ResourceRUClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/network-service")


class ICAPEnvironmentClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/icap-environments")


class KerberosEnvironmentClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/kerberos-environments")

    def connect_back_end_group(self, resource_id: str, ref_id: str):
        return super().connect_to_resources(resource_id, ref_id, "back-end-group")

    def disconnect_back_end_group(self, resource_id: str, ref_id: str):
        return super().disconnect_to_resources(resource_id, ref_id, "back-end-group")


class AllowedNetworkEnvironmentClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/allowed-network-endpoints")


class APIPolicyServiceClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/api-policy-services")

    def connect_mapping(self, resource_id: str, ref_id: str):
        return super().connect_to_resources(resource_id, ref_id, "mapping")

    def disconnect_mapping(self, resource_id: str, ref_id: str):
        return super().disconnect_to_resources(resource_id, ref_id, "mapping")


class LogSettingsClient(ResourceRUClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/log")


class ReportingSettingsClient(ResourceRUClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/reporting")


class ValidatorMessageClient(ResourceCRUDClient):
    def __init__(self, session: type(AirlockSession)):
        super().__init__(session, "/airlock/rest/configuration/validator-messages")
