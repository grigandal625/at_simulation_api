from fastapi import Depends
from sqlalchemy.orm import Session

from at_simulation_api.providers.visio import get_visio_service
from at_simulation_api.repository.editor.resource.repository import ResourceRepository
from at_simulation_api.service.editor.resource.service import ResourceService
from at_simulation_api.storage.postgres.storage import get_db


def get_resource_repository(session: Session = Depends(get_db)) -> ResourceRepository:
    return ResourceRepository(session)


def get_resource_service(
    resource_rep=Depends(get_resource_repository),
    visio_service=Depends(get_visio_service),
) -> ResourceService:
    return ResourceService(resource_rep, visio_service)
