from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.settings import settings
from routers import reading, item, author, core
import py_eureka_client.eureka_client as eureka_client

# Configurações do Eureka
EUREKA_SERVER = "http://localhost:8761/eureka"
APP_NAME = "library-service"
PORT = 8000

app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.project_version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

async def register_service():
    # Iniciar o cliente Eureka e registrar o serviço
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name=APP_NAME,
        instance_port=PORT
    )

@app.on_event("startup")
async def on_startup():
    # Registrar o serviço no Eureka quando o FastAPI iniciar
    await register_service()

app.include_router(item.router)
app.include_router(reading.router)
app.include_router(core.router)
app.include_router(author.router)
