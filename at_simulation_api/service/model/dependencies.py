from typing import List, Protocol

from at_simulation_api.repository.editor.function.models.models import FunctionDB
from at_simulation_api.repository.editor.resource.models.models import (
    ResourceDB,
    ResourceTypeDB,
)
from at_simulation_api.repository.editor.template.models.models import TemplateUsageDB
from at_simulation_api.repository.model.models.models import ModelMetaDB
from at_simulation_api.repository.model.repository import ModelRepository
from at_simulation_api.service.editor.function.service import FunctionService
from at_simulation_api.service.editor.resource.service import ResourceService
from at_simulation_api.service.editor.template.models.models import Templates
from at_simulation_api.service.editor.template.service import TemplateService


class IModelRepository(Protocol):
    def create_model(self, model: ModelMetaDB) -> int: ...

    def get_model_meta(self, model_id: int) -> ModelMetaDB: ...

    def get_models(self, user_id: int) -> List[ModelMetaDB]: ...

    def update_model(self, model: ModelMetaDB) -> int: ...

    def delete_model(self, model_id: int) -> int: ...


_: IModelRepository = ModelRepository(...)  # type: ignore[arg-type, reportArgumentType]


class IResourceService(Protocol):
    def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]: ...

    def get_resources(self, model_id: int) -> List[ResourceDB]: ...


_: IResourceService = ResourceService(..., ...)  # type: ignore[arg-type, reportArgumentType]


class IFunctionService(Protocol):
    def get_functions(self, model_id: int) -> List[FunctionDB]: ...


_: IFunctionService = FunctionService(..., ...)  # type: ignore[arg-type, reportArgumentType]


class ITemplateService(Protocol):
    def get_templates(self, model_id: int) -> Templates: ...

    def get_template_usages(self, model_id: int) -> List[TemplateUsageDB]: ...


_: ITemplateService = TemplateService(..., ...)  # type: ignore[arg-type, reportArgumentType]
