from typing import Annotated

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from at_simulation_api.client.auth_client import AuthClientSingleton
from at_simulation_api.delivery.model.dependencies import get_current_user
from at_simulation_api.delivery.processor.dependencies import IProcessorService
from at_simulation_api.delivery.processor.models.conversions import (
    to_ProcessesResponse,
    to_ProcessResponse,
)
from at_simulation_api.delivery.processor.models.models import (
    CreateProcessRequest,
    ProcessesResponse,
    ProcessResponse,
    RunProcessRequest,
)
from at_simulation_api.providers.processor import get_processor_service
from at_simulation_api.providers.websocket_manager import get_websocket_manager
from at_simulation_api.service.websocket_manager.service import WebsocketManager

router = APIRouter(
    prefix="/processor",
    tags=["processor"],
)


@router.post("", response_model=ProcessResponse)
def create_process(
    body: CreateProcessRequest,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> ProcessResponse:
    return to_ProcessResponse(
        processor_service.create_process(user_id, body.file_id, body.process_name)
    )


@router.post("/{process_id}/run", response_model=ProcessResponse | None)
async def run_process(
    process_id: str,
    body: RunProcessRequest,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
    websocket_manager: WebsocketManager = Depends(get_websocket_manager),
) -> ProcessResponse | None:
    try:
        data = await processor_service.run_process(
            user_id, process_id, body.ticks, body.delay
        )
        return to_ProcessResponse(data)
    except WebSocketDisconnect:
        await websocket_manager.disconnect(user_id, process_id)
        return None


@router.post("/{process_id}/pause", response_model=ProcessResponse)
def pause_process(
    process_id: str,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> ProcessResponse:
    return to_ProcessResponse(processor_service.pause_process(user_id, process_id))


@router.post("/{process_id}/kill", response_model=ProcessResponse)
def kill_process(
    process_id: str,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> ProcessResponse:
    return to_ProcessResponse(processor_service.kill_process(user_id, process_id))


@router.get("", response_model=ProcessesResponse)
def get_processes(
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> ProcessesResponse:
    return to_ProcessesResponse(processor_service.get_processes(user_id))


@router.get("/ws", summary="WebSocket Init")
def websocket_documentation():
    """
    ## WebSocket Documentation for `ws://<host>:<port>/api/processor/ws`

    - **WebSocket Endpoint**: `ws://<host>:<port>/api/processor/ws`
    - **Description**: Streams real-time updates for a process.

    ### Query parameters:
    - `process_id: str`
    - `token: str`

    ### Example Messages:
    - **Server Message**:
    ```json
    {
    "current_tick": 1,
    "resources": [
        {
        "resource_name": "vlados_ruble",
        "currency": 55,
        "<attr_name>": "<attr_value>",
        ...,
        },
        null,
        {
        "resource_name": "car_1",
        "pos_x": -20,
        "pos_y": 25,
        "<attr_name>": "<attr_value>",
        ...,
        },
        {
        "resource_name": "car_2",
        "pos_x": -20,
        "pos_y": 50,
        "<attr_name>": "<attr_value>",
        ...,
        }
    ],
    "usages": [
        {
        "has_triggered": true,
        "usage_name": "irregular_event_1",
        "usage_type": "IRREGULAR_EVENT"
        },
        {
        "has_triggered": false,
        "usage_name": "irregular_event_2",
        "usage_type": "IRREGULAR_EVENT"
        },
        {
        "has_triggered": false,
        "usage_name": "irregular_event_3",
        "usage_type": "IRREGULAR_EVENT"
        },
        {
        "has_triggered": false,
        "usage_name": "irregular_event_4",
        "usage_type": "IRREGULAR_EVENT"
        },
        {
        "has_triggered_after": false,
        "has_triggered_before": false,
        "usage_name": "operation_1",
        "usage_type": "OPERATION"
        },
        {
        "has_triggered_after": false,
        "has_triggered_before": false,
        "usage_name": "operation_2",
        "usage_type": "OPERATION"
        },
        {
        "has_triggered": true,
        "usage_name": "rule_1",
        "usage_type": "RULE"
        },
        {
        "has_triggered": false,
        "usage_name": "rule_2",
        "usage_type": "RULE"
        }
    ]
    }
    ```

    This endpoint does not return data directly as it is intended for documentation purposes.
    """
    return {}


@router.websocket("/ws")
async def websocket_init(
    websocket: WebSocket,
    token: Annotated[str | None, Query()] = None,
    process_id: Annotated[str | None, Query()] = None,
    websocket_manager: WebsocketManager = Depends(get_websocket_manager),
):
    if not token:
        await websocket.close(code=1008, reason="Missing token")
        return

    try:
        auth_client = await AuthClientSingleton.get_instance()
        user_id = await auth_client.verify_token(token)
    except Exception as e:
        await websocket.close(code=1008, reason="Invalid authentication")
        return

    if process_id is None:
        await websocket.close(code=1008, reason="Missing process_id")
        return

    await websocket_manager.connect(websocket, user_id, process_id)

    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket_manager.disconnect(user_id, process_id)
