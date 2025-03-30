from fastapi import Depends
from sqlalchemy.orm import Session

from at_simulation_api.providers.visio import get_visio_service
from at_simulation_api.repository.editor.function.repository import FunctionRepository
from at_simulation_api.service.editor.function.service import FunctionService
from at_simulation_api.storage.postgres.storage import get_db


def get_function_repository(session: Session = Depends(get_db)) -> FunctionRepository:
    return FunctionRepository(session)


def get_function_service(
    function_rep=Depends(get_function_repository),
    visio_service=Depends(get_visio_service),
) -> FunctionService:
    return FunctionService(function_rep, visio_service)
