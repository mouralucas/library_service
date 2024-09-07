from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.settings import settings
from routers import reading, item, author, core
import py_eureka_client.eureka_client as eureka_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Register the library in the Eureka
    await eureka_client.init_async(
        eureka_server=settings.eureka_host_name,
        app_name=settings.project_name,
        instance_port=settings.library_host_port,
        instance_host=settings.library_host_ip,
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
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(item.router)
app.include_router(reading.router)
app.include_router(core.router)
app.include_router(author.router)
