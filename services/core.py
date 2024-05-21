from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from managers.core import LanguageManager
from models import LanguageModel
from schemas.core import LanguageSchema
from schemas.request.core import CreateLanguageRequest
from schemas.response.core import CreateLanguageResponse
from services.base import BaseService


class LanguageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_language(self, language: CreateLanguageRequest) -> CreateLanguageResponse:
        new_language = await LanguageManager(session=self.session).create_language(LanguageModel(**language.dict()))

        response = CreateLanguageResponse(
            status_code=status.HTTP_201_CREATED,
            language=LanguageSchema.model_validate(new_language)
        )

        return response
