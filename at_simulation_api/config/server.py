from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class ServerConfig(BaseSettings):
    port: int = Field(..., alias="SERVER_PORT")

    class Config:
        extra = "allow"


class ServerConfigurator:
    @classmethod
    @lru_cache(maxsize=1)
    def get_server_config(cls) -> ServerConfig:
        return ServerConfig()
