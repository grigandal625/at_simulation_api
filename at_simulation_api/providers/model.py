from fastapi import Depends
from sqlalchemy.orm import Session

from at_simulation_api.providers.function import get_function_service
from at_simulation_api.providers.resource import get_resource_service
from at_simulation_api.providers.template import get_template_service
from at_simulation_api.repository.model.repository import ModelRepository
from at_simulation_api.service.model.service import ModelService
from at_simulation_api.storage.postgres.storage import get_db


def get_model_repository(session: Session = Depends(get_db)) -> ModelRepository:
    return ModelRepository(session)


def get_model_service(
    model_rep: ModelRepository = Depends(get_model_repository),
    resource_service=Depends(get_resource_service),
    template_service=Depends(get_template_service),
    function_service=Depends(get_function_service),
) -> ModelService:
    return ModelService(
        model_rep,
        resource_service,
        template_service,
        function_service,
    )
