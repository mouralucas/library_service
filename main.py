from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.settings import settings
from routers import reading, item, author, core
import py_eureka_client.eureka_client as eureka_client

# Configurações do Eureka
EUREKA_SERVER = "http://192.168.0.29:8761/eureka"
APP_NAME = "library-service"
PORT = 9001

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Registro no Eureka ao iniciar o ciclo de vida
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name="my-fastapi-service",
        instance_port=8001,
        instance_host='192.168.0.29',
    )
    try:
        yield
    finally:
        await eureka_client.stop_async()

app = FastAPI(
    title=settings.project_title,
    description=settings.project_description,
    version=settings.project_version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan,
)



app.include_router(item.router)
app.include_router(reading.router)
app.include_router(core.router)
app.include_router(author.router)
