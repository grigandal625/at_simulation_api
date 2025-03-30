from fastapi import Depends
from sqlalchemy.orm import Session

from at_simulation_api.repository.editor.imports.repository import ImportRepository
from at_simulation_api.service.editor.imports.service import ImportService
from at_simulation_api.storage.postgres.storage import get_db


def get_import_repository(session: Session = Depends(get_db)) -> ImportRepository:
    return ImportRepository(session)


def get_import_service(
    import_rep=Depends(get_import_repository),
) -> ImportService:
    return ImportService(import_rep)
