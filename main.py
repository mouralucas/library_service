from fastapi import FastAPI

from routers import reading, item

app = FastAPI(
    title="Library Service",
    description="This service implements all library operations",
    version='0.0.1',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(item.router)
app.include_router(reading.router)
