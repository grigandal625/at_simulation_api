from typing import List, Protocol

from at_simulation_api.repository.editor.function.models.models import FunctionDB
from at_simulation_api.service.editor.function.service import FunctionService


class IFunctionService(Protocol):
    def create_function(self, function: FunctionDB) -> int: ...

    def get_function(self, function_id: int, model_id: int) -> FunctionDB: ...

    def get_functions(self, model_id: int) -> List[FunctionDB]: ...

    def update_function(self, function: FunctionDB) -> int: ...

    def delete_function(self, function_id: int, model_id: int) -> int: ...


_: IFunctionService = FunctionService(..., ...)  # type: ignore[arg-type, reportArgumentType]
