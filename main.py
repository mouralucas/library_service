import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from rolf_common.base_middleware import LogsMiddleware
from starlette.middleware.cors import CORSMiddleware

from backend.settings import settings
from lifespan import shutdown_log_service, start_log_service
from routers import author, core, health_check, item, reading
from routers import graphql as graphql_library
from routers import graphql_v2 as graphql_library_v2

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
    root_path="/api/" + settings.project_name,
    lifespan=lifespan,
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogsMiddleware)

app.include_router(core.router)
app.include_router(item.router)
app.include_router(reading.router)
app.include_router(author.router)
app.include_router(health_check.router)

app.include_router(graphql_library.router)
app.include_router(graphql_library_v2.router)

