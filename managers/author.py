from sqlalchemy.ext.asyncio import AsyncSession

from managers.base import BaseDataManager
from models import SQLModel, AuthorModel


class AuthorManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_author(self, author: AuthorModel) -> SQLModel:
        """
        :Name: create_author
        :Created by: Lucas Penha de Moura - 21/05/2024
            Create a new author

            Params:
                language: an instance of AuthorModel
        """
        new_author = await self.add_one(author)

        return new_author
