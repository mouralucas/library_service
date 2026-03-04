
from fastapi import APIRouter

router = APIRouter(prefix="/author", tags=["Author"])


# @router.post("", status_code=status.HTTP_201_CREATED)
# async def create_author(
#     author: CreateAuthorRequest,
#     session: AsyncSession = Depends(get_session),
#     user: RequiredUser = Security(get_user),
# ) -> dict[str, Any]:
#     response = await AuthorService(session).create_author(author=author)

#     return response
