from typing import List

from at_simulation_api.delivery.processor.models.models import (
    ProcessesResponse,
    ProcessResponse,
    ProcessStatusEnum,
)
from at_simulation_api.service.processor.models.models import Process


def to_ProcessResponse(process: Process) -> ProcessResponse:
    return ProcessResponse(
        id=process.process_id,
        name=process.process_name,
        file_id=process.file_uuid,
        status=ProcessStatusEnum(process.status.value),
        current_tick=process.current_tick,
    )


def to_ProcessesResponse(processes: List[Process]) -> ProcessesResponse:
    return ProcessesResponse(
        processes=[to_ProcessResponse(process) for process in processes],
        total=len(processes),
    )
