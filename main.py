from fastapi import FastAPI

from backend.settings import settings
from routers import reading, item, author, core

app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.project_version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


@app.middleware(middleware_type="http")
async def validate_request_middleware(request, call_next):
    async def check_token():
        _authorization = request.headers.get('authorization')
        _path = request.url.path
        _required_auth_endpoints = ['/reading', '/reading/progress']
        if not _authorization and _path not in _required_auth_endpoints:
            print('No need auth')
        else:
            print('Need auth')

    await check_token()

    response = await call_next(request)
    return response


app.include_router(item.router)
app.include_router(reading.router)
app.include_router(core.router)
app.include_router(author.router)
