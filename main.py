import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from rolf_common.base_middleware import LogsMiddleware
from starlette.middleware.cors import CORSMiddleware

from backend.settings import settings
from lifespan import start_log_service, shutdown_log_service
from routers import reading, item, author, core


# import py_eureka_client.eureka_client as eureka_client


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Register the library in the Eureka
#     await eureka_client.init_async(
#         eureka_server=settings.eureka_host_name,
#         app_name=settings.project_name,
#         instance_port=settings.library_host_port,
#         instance_host=settings.library_host_ip,
#     )
#
#     try:
#         yield
#     finally:
#         await eureka_client.stop_async()
@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.gather(
        start_log_service(),
    )

    try:
        yield
    finally:
        await asyncio.gather(
            shutdown_log_service(),
        )


app = FastAPI(
    title=settings.project_title,
    description=settings.project_description,
    version=settings.project_version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/",
    root_path='/api/' + settings.project_name,
    lifespan=lifespan,
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:80",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogsMiddleware)

app.include_router(item.router)
app.include_router(reading.router)
app.include_router(core.router)
app.include_router(author.router)
