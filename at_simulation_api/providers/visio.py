from fastapi import Depends
from sqlalchemy.orm import Session

from at_simulation_api.repository.visio.repository import VisioRepository
from at_simulation_api.service.visio.service import VisioService
from at_simulation_api.storage.postgres.storage import get_db


def get_visio_repository(session: Session = Depends(get_db)) -> VisioRepository:
    return VisioRepository(session)


def get_visio_service(visio_rep=Depends(get_visio_repository)) -> VisioService:
    return VisioService(visio_rep)
