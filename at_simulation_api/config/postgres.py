from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    host: str = Field(..., alias="DB_HOST")
    port: int = Field(..., alias="DB_PORT")
    name: str = Field(..., alias="DB_NAME")
    user: str = Field(..., alias="DB_USER")
    password: str = Field(..., alias="DB_PASS")

    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        extra = "allow"


class PostgresStore:
    @classmethod
    @lru_cache(maxsize=1)
    def get_database_config(cls) -> DatabaseConfig:
        return DatabaseConfig()
