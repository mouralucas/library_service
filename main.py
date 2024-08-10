from fastapi import FastAPI

from backend.settings import settings
from routers import reading, item, author, core

app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.project_version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


app.include_router(item.router)
app.include_router(reading.router)
app.include_router(core.router)
app.include_router(author.router)
