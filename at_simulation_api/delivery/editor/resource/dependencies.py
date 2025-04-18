from typing import List, Protocol

from at_simulation_api.repository.editor.resource.models.models import (
    ResourceDB,
    ResourceTypeDB,
)
from at_simulation_api.service.editor.resource.service import ResourceService


class IResourceService(Protocol):
    def create_resource_type(self, resource_type: ResourceTypeDB) -> int: ...

    def get_resource_type(
        self, resource_type_id: int, model_id: int
    ) -> ResourceTypeDB: ...

    def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]: ...

    def update_resource_type(self, resource_type: ResourceTypeDB) -> int: ...

    def delete_resource_type(self, resource_type_id: int, model_id: int) -> int: ...

    def create_resource(self, resource: ResourceDB) -> int: ...

    def get_resource(self, resource_id: int, model_id: int) -> ResourceDB: ...

    def get_resources(self, model_id: int) -> List[ResourceDB]: ...

    def update_resource(self, resource: ResourceDB) -> int: ...

    def delete_resource(self, resource_id: int, model_id: int) -> int: ...


_: IResourceService = ResourceService(..., ...)  # type: ignore[arg-type, reportArgumentType]
