from typing import List, Protocol

from at_simulation_api.repository.editor.function.models.models import FunctionDB
from at_simulation_api.repository.editor.function.repository import FunctionRepository
from at_simulation_api.repository.visio.models.models import NodeTypesEnum
from at_simulation_api.service.visio.service import VisioService


class IFunctionRepository(Protocol):
    def create_function(self, function: FunctionDB) -> int: ...

    def get_function(self, function_id: int) -> FunctionDB: ...

    def get_functions(self, model_id: int) -> List[FunctionDB]: ...

    def update_function(self, function: FunctionDB) -> int: ...

    def delete_function(self, function_id: int) -> int: ...


_: IFunctionRepository = FunctionRepository(...)  # type: ignore[arg-type, reportArgumentType]


class IVisioService(Protocol):
    def create_node(
        self, object_id: int, object_name: str, node_type: NodeTypesEnum, model_id: int
    ) -> int: ...

    def update_node_name(
        self, object_id: int, object_name: str, node_type: NodeTypesEnum
    ) -> int: ...


_: IVisioService = VisioService(...)  # type: ignore[arg-type, reportArgumentType]
