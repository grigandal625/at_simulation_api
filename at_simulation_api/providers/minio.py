from fastapi import Depends

from at_simulation_api.repository.minio.repository import MinioRepository
from at_simulation_api.storage.minio.storage import get_minio_storage


def get_minio_repository(minio_info=Depends(get_minio_storage)) -> MinioRepository:
    client, bucket_name = minio_info
    return MinioRepository(client, bucket_name)
