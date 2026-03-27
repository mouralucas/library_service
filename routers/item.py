from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from rolf_common.schemas.auth import RequiredUser
from rolf_common.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_session
from schemas.request.item import UpdateItemRequest
from schemas.response.item import CreateItemResponse
from services.item import ItemService

router = APIRouter(prefix="/item", tags=["Items"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.patch("", description="Update item")
async def update_item(
    item: UpdateItemRequest,
    session: AsyncSession = Depends(get_session),
    user: RequiredUser = Security(get_user),
) -> CreateItemResponse:
    response = await ItemService(session=session, user=user).update_item(item)

    return response
