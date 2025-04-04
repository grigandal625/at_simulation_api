from fastapi import APIRouter, Depends

from at_simulation_api.delivery.model.dependencies import get_current_model
from at_simulation_api.delivery.visio.dependencies import IVisioService
from at_simulation_api.delivery.visio.models.conversions import (
    to_EditorInfoResponse,
    to_MoveNodeDB,
)
from at_simulation_api.delivery.visio.models.models import (
    EditorInfoResponse,
    MoveNodeRequest,
)
from at_simulation_api.providers.visio import get_visio_service

router = APIRouter(
    prefix="/visio",
    tags=["visio"],
)


@router.get("/editor/info", response_model=EditorInfoResponse)
async def get_editor_info(
    model_id: int = Depends(get_current_model),
    visio_service: IVisioService = Depends(get_visio_service),
) -> EditorInfoResponse:
    return to_EditorInfoResponse(visio_service.get_editor_info(model_id))


@router.patch("/editor/nodes/{node_id}/move", response_model=None)
async def move_node(
    body: MoveNodeRequest,
    node_id: int,
    model_id: int = Depends(get_current_model),
    visio_service: IVisioService = Depends(get_visio_service),
) -> None:
    visio_service.move_node(to_MoveNodeDB(body, node_id), model_id)
