from typing import Protocol

from at_simulation_api.repository.visio.models.models import EditorInfoDB, MoveNodeDB
from at_simulation_api.service.visio.service import VisioService


class IVisioService(Protocol):
    def get_editor_info(self, model_id: int) -> EditorInfoDB: ...

    def move_node(self, params: MoveNodeDB, model_id: int) -> None: ...


_: IVisioService = VisioService(...)  # type: ignore[arg-type, reportArgumentType]
