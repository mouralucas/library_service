from typing import Any

from managers.author import AuthorManager
from models import AuthorModel
from schemas.item import AuthorSchema
from schemas.request.author import CreateAuthorRequest, GetAuthorsRequest
from schemas.response.author import CreateAuthorResponse
from services.base import BaseService


class AuthorService(BaseService):
    def __init__(self, session):
        super().__init__(session=session)

    async def create_author(self, author: CreateAuthorRequest) -> CreateAuthorResponse:
        new_author = await AuthorManager(session=self.session).create_author(
            AuthorModel(**author.model_dump())
        )

        response = CreateAuthorResponse(
            author=AuthorSchema.model_validate(new_author),
        )

        return response

    async def get_authors(self, params: GetAuthorsRequest) -> dict[str, Any]:
        authors = await AuthorManager(session=self.session).get_authors()

        response = {"quantity": len(authors) if authors else 0, "authors": authors}

        return response
