from sqlalchemy import select
from starlette import status

from managers.author import AuthorManager
from models import AuthorModel
from schemas.item import AuthorSchema
from schemas.request.author import CreateAuthorRequest
from schemas.response.author import CreateAuthorResponse, GetAuthorResponse
from services.base import BaseService


class AuthorService(BaseService):
    def __init__(self, session):
        super().__init__(session=session)

    async def create_author(self, author: CreateAuthorRequest) -> CreateAuthorResponse:
        new_author = await AuthorManager(session=self.session).create_author(AuthorModel(**author.model_dump()))

        response = CreateAuthorResponse(
            status_code=status.HTTP_201_CREATED,
            author=AuthorSchema.model_validate(new_author)
        )

        return response

    async def get_author(self) -> GetAuthorResponse:
        stmt = select(AuthorModel)

        authors = await AuthorManager(session=self.session).get_all(select_statement=stmt)

        response = GetAuthorResponse(
            status_code=status.HTTP_200_OK,
            quantity=len(authors) if authors else 0,
            authors=[AuthorSchema.model_validate(author) for author in authors] if authors else []
        )

        return response
