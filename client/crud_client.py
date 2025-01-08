from .airlock_session import AirlockSession

class ResourceRUClient:
    def __init__(self, session: type(AirlockSession), base_path: str):
        self.client = session
        self.base_path = base_path

    def get(self):
        return self.client.get(self.base_path)

    def update(self, data):
        return self.client.patch(
            path=self.base_path,
            data=data
        )


class ResourceCRUDClient:
    def __init__(self, session: type(AirlockSession), base_path: str):
        self.client = session
        self.base_path = base_path

    def all(self):
        return self.client.get(self.base_path)

    def get(self, resource_id: str):
        return self.client.get(f"{self.base_path}/{resource_id}")

    def create(self, data):
        return self.client.post(
            path=self.base_path,
            data=data
        )

    def update(self, resource_id: str, data):
        return self.client.patch(
            path=f"{self.base_path}/{resource_id}",
            data=data
        )

    def delete(self, resource_id: str):
        return self.client.delete(f"{self.base_path}/{resource_id}")

    def connect_to_resources(self, resource_id: str, relationship_id: str, relationship_type: str):
        return self.connect_to_resources(resource_id, relationship_id, relationship_type + "s", relationship_type)

    def connect_to_resources(self, resource_id: str, relationship_id: str, path: str, relationship_type: str):
        return self.client.patch(
            path=f"{self.base_path}/{resource_id}/relationships/{path}",
            data=(
                "{"
                "\"data\" : [{"
                f"\"type\" : \"{relationship_type}\","
                f"\"id\" : \"{relationship_id}\""
                "}]"
                "}"
            )
        )

    def connect_to_resource(self, resource_id: str, relationship_id: str, relationship_type: str):
        return self.client.patch(
            path=f"{self.base_path}/{resource_id}/relationships/{relationship_type}",
            data=(
                "{"
                "\"data\" : {"
                f"\"type\" : \"{relationship_type}\","
                f"\"id\" : \"{relationship_id}\""
                "}"
                "}"
            )
        )

    def disconnect_to_resources(self, resource_id: str, relationship_id: str, relationship_type: str):
        return self.disconnect_to_resource(resource_id, relationship_id, relationship_type + "s", relationship_type)

    def disconnect_to_resources(self, resource_id: str, relationship_id: str, path: str, relationship_type: str):
        return self.client.delete(
            path=f"{self.base_path}/{resource_id}/relationships/{path}",
            data=(
                "{"
                "\"data\" : [{"
                f"\"type\" : \"{relationship_type}\","
                f"\"id\" : \"{relationship_id}\""
                "}]"
                "}"
            )
        )

    def disconnect_to_resource(self, resource_id: str, relationship_id: str, relationship_type: str):
        return self.client.delete(
            path=f"{self.base_path}/{resource_id}/relationships/{relationship_type}",
            data=(
                "{"
                "\"data\" : {"
                f"\"type\" : \"{relationship_type}\","
                f"\"id\" : \"{relationship_id}\""
                "}"
                "}"
            )
        )
