

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers.item_v2 import ItemManagerV2
from services.base import BaseService


class ItemServiceV2(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.item_manager = ItemManagerV2(session=session)
        
    async def get_editions(
        self, 
        owner_id: uuid.UUID,
        metadata_id: uuid.UUID | None = None
    ):
        editions = await self.item_manager.get_editions(owner_id=owner_id)
        
        return editions