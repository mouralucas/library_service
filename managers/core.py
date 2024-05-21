from sqlalchemy.ext.asyncio import AsyncSession

from managers.base import BaseDataManager
from models import LanguageModel, SQLModel


class LanguageManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create_language(self, language: LanguageModel) -> SQLModel:
        """
        :Name: update_one
        :Created by: Lucas Penha de Moura - 20/05/2024
            Create a new language

            Params:
                language: a instance of LanguageModel
        """
        new_language = await self.add_one(language)

        return new_language
