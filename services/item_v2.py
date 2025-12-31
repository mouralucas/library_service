import uuid
from typing import Any

from rolf_common.schemas.auth import RequiredUser
from sqlalchemy.ext.asyncio import AsyncSession

from managers.item_v2 import ItemManagerV2
from services.base import BaseService


class ItemServiceV2(BaseService):
    def __init__(self, session: AsyncSession, user: RequiredUser) -> None:
        super().__init__(session)
        self.user = user.model_dump()
        self.item_manager = ItemManagerV2(session=session)

    async def get_editions(
        self, owner_id: uuid.UUID, metadata_id: uuid.UUID | None = None
    ) -> dict[str, Any]:
        editions = await self.item_manager.get_editions(owner_id=owner_id)

        metadata: dict[str, dict] = {}
        for row in editions or []:
            metadata_id_ = row["metadata_id"]

            if metadata_id_ not in metadata:
                metadata[metadata_id_] = {
                    "metadata_id": metadata_id_,
                    "title": None,  # resolver depois
                    "main_author": row["main_author_name"],
                    "original_language_id": row["language_id"],
                    "original_language_name": row["language_name"],
                    "item_type_id": row["item_type_id"],
                    "item_type_name": row["item_type_name"],
                    "serie_id": row["serie_id"],
                    "serie_name": row["serie_name"],
                    "editions": [],
                }

            metadata[metadata_id_]["editions"].append(
                {
                    "metadata_id": metadata_id_,
                    "title": row["title"],
                    "subtitle": row["subtitle"],
                    "isbn": row["isbn"],
                    "pages": row["pages"],
                    "format": row["format_name"],
                    "language": row["language_name"],
                    "publisher": row["publisher_name"],
                    "collection": row["collection_name"],
                }
            )

        return {"editions": list(metadata.values()) if metadata else []}

        # return list(metadata.values()) if metadata else []
