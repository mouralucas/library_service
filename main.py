from fastapi import FastAPI

from routers import reading, item

from backend.settings import get_settings

app = FastAPI(
    title=get_settings().APP_SETTINGS.name,
    description=get_settings().APP_SETTINGS.description,
    version=get_settings().APP_SETTINGS.version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


@app.middleware(middleware_type="http")
async def validate_request_middleware(request, call_next):
    async def check_token():
        # TODO: check login here? Maybe create this check in gateway service
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
