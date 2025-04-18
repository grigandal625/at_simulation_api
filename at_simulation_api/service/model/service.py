from typing import List

from at_simulation_api.core.errors import ForbiddenError, WrapMethodsMeta
from at_simulation_api.repository.model.models.models import ModelMetaDB
from at_simulation_api.service.model.dependencies import (
    IFunctionService,
    IModelRepository,
    IResourceService,
    ITemplateService,
)
from at_simulation_api.service.model.models.conversions import to_Model
from at_simulation_api.service.model.models.models import Model


class ModelService(metaclass=WrapMethodsMeta):
    def __init__(
        self,
        model_rep: IModelRepository,
        resource_service: IResourceService,
        template_service: ITemplateService,
        function_service: IFunctionService,
    ) -> None:
        self._model_rep = model_rep
        self._resource_service = resource_service
        self._template_service = template_service
        self._function_service = function_service

    def check_model_rights(self, model_id: int, user_id: int) -> None:
        model = self._model_rep.get_model_meta(model_id)
        if model.user_id != user_id:
            raise ForbiddenError(f"Model {model_id} does not belong to user {user_id}")

    def create_model(self, model: ModelMetaDB) -> int:
        return self._model_rep.create_model(model)

    def get_models(self, user_id: int) -> List[ModelMetaDB]:
        return self._model_rep.get_models(user_id)

    def update_model(self, model: ModelMetaDB) -> int:
        self.check_model_rights(model.id, model.user_id)
        return self._model_rep.update_model(model)

    def delete_model(self, model_id: int, user_id: int) -> int:
        self.check_model_rights(model_id, user_id)
        return self._model_rep.delete_model(model_id)

    def get_model(self, model_id: int, user_id: int) -> Model:
        self.check_model_rights(model_id, user_id)

        meta = self._model_rep.get_model_meta(model_id)
        resource_types = self._resource_service.get_resource_types(model_id)
        resources = self._resource_service.get_resources(model_id)
        templates = self._template_service.get_templates(model_id)
        template_usages = self._template_service.get_template_usages(model_id)
        functions = self._function_service.get_functions(model_id)

        return to_Model(
            meta, resource_types, resources, templates, template_usages, functions
        )
