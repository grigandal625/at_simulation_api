import asyncio
from contextlib import asynccontextmanager

import uvicorn
from at_queue.core.session import ConnectionParameters
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from at_simulation_api.client.auth_client import AuthClientSingleton
from at_simulation_api.config.cli_args import parse_args
from at_simulation_api.config.rabbitmq import RabbitMQStore
from at_simulation_api.config.server import ServerConfigurator
from at_simulation_api.delivery.core.middleware.fastapi_exception_handler import (
    validation_exception_handler,
)
from at_simulation_api.delivery.core.middleware.logging import LoggingMiddleware
from at_simulation_api.delivery.core.middleware.response import ResponseMiddleware
from at_simulation_api.delivery.router import setup_routes
from at_simulation_api.providers.model import get_model_service
from at_simulation_api.providers.processor import get_processor_service
from at_simulation_api.providers.translator import get_translator_service
from at_simulation_api.worker.worker import ATSimulationWorker


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_routes(app)
    # Initialize resources like database connections
    # setup_storage()

    auth_client = await AuthClientSingleton.get_instance()
    loop = asyncio.get_event_loop()
    task = loop.create_task(auth_client.start())

    rabbitmq_config = RabbitMQStore.get_rabbitmq_config()
    connection_parameters = ConnectionParameters(rabbitmq_config.url)
    simulation_worker = ATSimulationWorker(
        connection_parameters=connection_parameters,
        auth_client=auth_client,
        model_service=Depends(get_model_service),
        translator_service=Depends(get_translator_service),
        processor_service=Depends(get_processor_service),
    )

    await simulation_worker.initialize()
    await simulation_worker.register()

    task = asyncio.create_task(simulation_worker.start())

    try:
        yield
    finally:
        task.cancel()

    # Cleanup resources
    # shutdown_storage()
    pass


app = FastAPI(title="AT_SIMULATION", version="1.0.0", lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ResponseMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.exception_handler(RequestValidationError)(validation_exception_handler)


if __name__ == "__main__":
    parse_args()
    server_config = ServerConfigurator().get_server_config()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=server_config.port,
    )
