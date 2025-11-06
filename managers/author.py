from typing import Any, cast

from rolf_common.managers import BaseDataManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import AuthorModel, CountryModel, LanguageModel


class AuthorManager(BaseDataManager):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_author(self, author: AuthorModel) -> AuthorModel:
        """
        :Name: create_author
        :Created by: Lucas Penha de Moura - 21/05/2024
            Create a new author

            Params:
                language: an instance of AuthorModel
        """
        new_author = await self.add_one(author)

        return cast(AuthorModel, new_author)

    async def get_authors(
        self, author_id: int | None = None
    ) -> list[dict[Any, Any]] | None:
        query = (
            select(
                AuthorModel.id,
                AuthorModel.name,
                AuthorModel.birth_date,
                AuthorModel.description,
                AuthorModel.country_id,
                CountryModel.name.label("country_name"),
                AuthorModel.language_id,
                LanguageModel.name.label("language_name"),
                AuthorModel.is_translator,
            )
            .select_from(AuthorModel)
            .outerjoin(CountryModel, AuthorModel.country_id == CountryModel.id)
            .outerjoin(LanguageModel, AuthorModel.language_id == LanguageModel.id)
            .order_by(AuthorModel.name)
        )

        if author_id:
            query.where(AuthorModel.id == author_id)

        authors = await self.get_all(select_statement=query)

        return [dict(author.items()) for author in authors] if authors else None
