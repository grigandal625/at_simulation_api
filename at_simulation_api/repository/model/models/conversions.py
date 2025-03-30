from at_simulation_api.repository.model.models.models import ModelMetaDB
from at_simulation_api.schema.model import Model


def to_ModelMetaDB(model: Model) -> ModelMetaDB:
    return ModelMetaDB(
        id=model.id,
        name=model.name,
        user_id=model.user_id,
        created_at=model.created_at,
    )


def to_Model(model: ModelMetaDB) -> Model:
    return Model(
        name=model.name,
        user_id=model.user_id,
    )
