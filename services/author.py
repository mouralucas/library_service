from managers.author import AuthorManager
from models import AuthorModel
from schemas.item import AuthorSchema
from schemas.request.author import CreateAuthorRequest, GetAuthorsRequest
from schemas.response.author import CreateAuthorResponse, GetAuthorResponse
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

    async def get_author(self, params: GetAuthorsRequest) -> GetAuthorResponse:
        authors = await AuthorManager(session=self.session).get_authors()

        response = GetAuthorResponse(
            quantity=len(authors) if authors else 0,
            authors=(
                [AuthorSchema.model_validate(author) for author in authors]
                if authors
                else []
            ),
        )

        return response
