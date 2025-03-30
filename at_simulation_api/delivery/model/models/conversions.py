from typing import List

from at_simulation_api.delivery.model.models.models import (
    ModelMetaRequest,
    ModelMetaResponse,
    ModelMetasResponse,
)
from at_simulation_api.repository.model.models.models import ModelMetaDB


def to_ModelMetaDB(model: ModelMetaRequest, user_id: int) -> ModelMetaDB:
    return ModelMetaDB(
        id=model.id or 0,
        name=model.name,
        user_id=user_id,
    )


def to_ModelMetaResponse(model: ModelMetaDB) -> ModelMetaResponse:
    return ModelMetaResponse(
        id=model.id,
        name=model.name,
        created_at=model.created_at,
    )


def to_ModelMetasResponse(models: List[ModelMetaDB]) -> ModelMetasResponse:
    return ModelMetasResponse(
        metas=[to_ModelMetaResponse(model) for model in models],
        total=len(models),
    )
