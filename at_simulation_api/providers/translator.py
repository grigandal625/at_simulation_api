from fastapi import Depends

from at_simulation_api.providers.minio import get_minio_repository
from at_simulation_api.providers.model import get_model_service
from at_simulation_api.repository.minio.repository import MinioRepository
from at_simulation_api.service.model.service import ModelService
from at_simulation_api.service.translator.service import TranslatorService


def get_translator_service(
    model_service: ModelService = Depends(get_model_service),
    file_repository: MinioRepository = Depends(get_minio_repository),
) -> TranslatorService:
    return TranslatorService(
        model_service,
        file_repository,
    )
