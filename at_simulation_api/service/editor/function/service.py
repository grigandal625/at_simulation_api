from typing import List

from at_simulation_api.core.errors import ForbiddenError, WrapMethodsMeta
from at_simulation_api.repository.editor.function.models.models import FunctionDB
from at_simulation_api.repository.visio.models.models import NodeTypesEnum
from at_simulation_api.service.editor.function.dependencies import (
    IFunctionRepository,
    IVisioService,
)
from at_simulation_api.service.helpers import handle_rollback


class FunctionService(metaclass=WrapMethodsMeta):
    def __init__(
        self,
        function_rep: IFunctionRepository,
        visio_service: IVisioService,
    ) -> None:
        self._function_rep = function_rep
        self._visio_service = visio_service

    def _check_function_rights(self, function_id: int, model_id: int) -> None:
        function = self._function_rep.get_function(function_id)
        if function.model_id != model_id:
            raise ForbiddenError(
                f"Function {function_id} does not belong to model {model_id}"
            )

    def create_function(self, function: FunctionDB) -> int:
        obj_id = self._function_rep.create_function(function)

        with handle_rollback(self._function_rep.delete_function, obj_id):
            self._visio_service.create_node(
                obj_id,
                function.name,
                NodeTypesEnum.FUNCTION,
                function.model_id,
            )

        return obj_id

    def get_function(self, function_id: int, model_id: int) -> FunctionDB:
        self._check_function_rights(function_id, model_id)
        return self._function_rep.get_function(function_id)

    def get_functions(self, model_id: int) -> List[FunctionDB]:
        return self._function_rep.get_functions(model_id)

    def update_function(self, function: FunctionDB) -> int:
        self._check_function_rights(function.id, function.model_id)
        original_function = self._function_rep.get_function(function.id)
        obj_id = self._function_rep.update_function(function)

        with handle_rollback(self.update_function, original_function):
            self._visio_service.update_node_name(
                obj_id,
                function.name,
                NodeTypesEnum.FUNCTION,
            )

        return obj_id

    def delete_function(self, function_id: int, model_id: int) -> int:
        self._check_function_rights(function_id, model_id)
        return self._function_rep.delete_function(function_id)
