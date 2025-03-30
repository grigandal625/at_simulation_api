from typing import List, Protocol

from at_simulation_api.repository.minio.models.models import MinioFile
from at_simulation_api.repository.minio.repository import MinioRepository
from at_simulation_api.service.model.models.models import Model
from at_simulation_api.service.model.service import ModelService


class IModelService(Protocol):
    def get_model(self, model_id: int, user_id: int) -> Model: ...

    def check_model_rights(self, model_id: int, user_id: int) -> None: ...


_: IModelService = ModelService(..., ..., ..., ...)  # type: ignore[arg-type, reportArgumentType]


class IFileRepository(Protocol):
    def load_file(
        self, user_id: int, file_path: str, file_name: str, model_id: int
    ) -> str: ...

    def get_files(self, user_id: int) -> List[MinioFile]: ...


_: IFileRepository = MinioRepository(..., ...)  # type: ignore[arg-type, reportArgumentType]
