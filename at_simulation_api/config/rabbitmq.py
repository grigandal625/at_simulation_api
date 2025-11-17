from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from yarl import URL


class RabbitMQConfig(BaseSettings):
    host: str = Field(..., alias="RABBITMQ_HOST")
    port: int = Field(..., alias="RABBITMQ_PORT")
    login: str = Field(..., alias="RABBITMQ_LOGIN")
    password: str = Field(..., alias="RABBITMQ_PASSWORD")
    virtualhost: str = Field(..., alias="RABBITMQ_VHOST")
    ssl: bool = Field(default=False, alias="RABBITMQ_SSL")

    @property
    def url(self) -> URL:
        scheme = "amqps" if str(self.ssl).strip().lower() in ['true', '1', 'yes', 'y', 't'] else "amqp"
        return URL.build(
            scheme=scheme,
            host=self.host,
            port=self.port,
            user=self.login,
            password=self.password,
            path=self.virtualhost,
        )

    class Config:
        extra = "allow"


class RabbitMQStore:
    @classmethod
    @lru_cache(maxsize=1)
    def get_rabbitmq_config(cls) -> RabbitMQConfig:
        return RabbitMQConfig()
