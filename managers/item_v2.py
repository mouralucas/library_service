import uuid
from typing import Any

from rolf_common.managers import BaseDataManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from models.core import (
    AuthorModel,
    CollectionModel,
    ItemFormatModel,
    ItemTypeModel,
    LanguageModel,
    PublisherModel,
    SerieModel,
)
from models.item import ItemEditionModel, ItemEditionUserModel, ItemMetadataModel


class ItemManagerV2(BaseDataManager):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    async def get_editions(
        self, owner_id: uuid.UUID, metadata_id: uuid.UUID | None = None
    ) -> list[dict[str, Any]] | None:
        item_metadata_alias = aliased(ItemMetadataModel)
        metadata_main_author_alias = aliased(AuthorModel)
        metadata_type_alias = aliased(ItemTypeModel)
        metadata_serie_alias = aliased(SerieModel)
        item_edition_alias = aliased(ItemEditionModel)
        edition_publisher_alias = aliased(PublisherModel)
        edition_language_alias = aliased(LanguageModel)
        edition_format_alias = aliased(ItemFormatModel)
        edition_user_alias = aliased(ItemEditionUserModel)
        edition_collection_alias = aliased(CollectionModel)

        query = (
            select(
                edition_user_alias.user_id.label("owner_id"),
                item_metadata_alias.id.label("metadata_id"),
                metadata_main_author_alias.id.label("main_author_id"),
                metadata_main_author_alias.name.label("main_author_name"),
                item_edition_alias.title,
                item_edition_alias.subtitle,
                item_edition_alias.isbn,
                item_edition_alias.pages,
                item_edition_alias.published_date,
                edition_publisher_alias.id.label("publisher_id"),
                edition_publisher_alias.name.label("publisher_name"),
                edition_language_alias.id.label("language_id"),
                edition_language_alias.name.label("language_name"),
                edition_format_alias.id.label("format_id"),
                edition_format_alias.name.label("format_name"),
                metadata_type_alias.id.label("item_type_id"),
                metadata_type_alias.name.label("item_type_name"),
                metadata_serie_alias.id.label("serie_id"),
                metadata_serie_alias.name.label("serie_name"),
                edition_collection_alias.id.label("collection_id"),
                edition_collection_alias.name.label("collection_name"),
            )
            .join(
                item_metadata_alias,
                item_metadata_alias.id == item_edition_alias.item_metadata_id,
            )
            .join(
                metadata_main_author_alias,
                metadata_main_author_alias.id == item_metadata_alias.main_author_id,
            )
            .join(
                edition_publisher_alias,
                edition_publisher_alias.id == item_edition_alias.publisher_id,
            )
            .join(
                edition_language_alias,
                edition_language_alias.id == item_edition_alias.language_id,
            )
            .outerjoin(
                edition_format_alias,
                edition_format_alias.id == item_edition_alias.format_id,
            )
            .join(
                metadata_type_alias,
                metadata_type_alias.id == item_metadata_alias.type_id,
            )
            .join(
                edition_user_alias,
                item_edition_alias.id == edition_user_alias.item_edition_id,
            )
            .join(
                edition_collection_alias,
                edition_collection_alias.id == item_edition_alias.collection_id,
            )
            .outerjoin(
                metadata_serie_alias,
                metadata_serie_alias.id == item_metadata_alias.serie_id,
            )
            .where(edition_user_alias.user_id == owner_id)
        )

        editions = await self.get_all(query)

        editions = [dict(i) for i in editions] if editions else None

        return editions
