from fastapi import Depends

from at_simulation_api.providers.minio import get_minio_repository
from at_simulation_api.providers.websocket_manager import get_websocket_manager
from at_simulation_api.service.processor.service import ProcessorService


def get_processor_service(
    file_repository=Depends(get_minio_repository),
    websocket_manager=Depends(get_websocket_manager),
) -> ProcessorService:
    return ProcessorService(
        file_repository,
        websocket_manager,
    )
