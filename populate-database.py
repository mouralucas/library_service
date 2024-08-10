import asyncio
import datetime
import uuid

from rolf_common.managers import BaseDataManager

from backend.database import sessionmanager
from managers.author import AuthorManager
from managers.core import LanguageManager, CountryManager, SerieManager, CollectionManager, PublisherManager
from managers.item import ItemManager
from models import StatusModel, LanguageModel, CountryModel, SerieModel, CollectionModel, PublisherModel, AuthorModel, ItemModel
import sqlalchemy.exc

async def insert_data():
    async with sessionmanager.session() as session:
        try:
            print('Inserting item status data...')
            await BaseDataManager(session=session).add_one(StatusModel(id='owned', name='Na estante', type='ITEM.STATUS'))
            await BaseDataManager(session=session).add_one(StatusModel(id='bought', name='Comprado', type='ITEM.STATUS'))
            await BaseDataManager(session=session).add_one(StatusModel(id='desired', name='Desejado', type='ITEM.STATUS'))
        except sqlalchemy.exc.PendingRollbackError:
            print('Item status data already inserted.')

        try:
            print('Inserting reading status data...')
            await BaseDataManager(session=session).add_one(StatusModel(id='reading', name='Lendo', type='READING.STATUS'))
            await BaseDataManager(session=session).add_one(StatusModel(id='read', name='Lido', type='READING.STATUS'))
        except Exception:
            print('Reading status data already inserted.')

        try:
            print('Inserting language data...')
            await LanguageManager(session=session).create_language(LanguageModel(id='EN', name='English', code='EN'))
            await LanguageManager(session=session).create_language(LanguageModel(id='PT', name='Portuguese', code='PT'))
        except Exception:
            print('Language data already inserted.')

        try:
            print('Inserting country data...')
            await CountryManager(session=session).create_country(CountryModel(id='BR', name='Brasil', continent='SA'))
            await CountryManager(session=session).create_country(CountryModel(id='DE', name='Alemanha', continent='EU'))
            await CountryManager(session=session).create_country(CountryModel(id='AU', name='Austrália', continent='OC'))
        except Exception:
            print('Country data already inserted.')

        try:
            print('Inserting serie data...')
            await SerieManager(session=session).create_serie(SerieModel(id=0, name='Default', description='Default serie'))
            await SerieManager(session=session).create_serie(SerieModel(id=1, name='Test serie', description='Test serie description'))
            await SerieManager(session=session).create_serie(SerieModel(id=2, name='Test serie 2', description='Test serie 2 description'))
        except Exception:
            print('Serie data already inserted.')

        try:
            print('Inserting collection data...')
            await CollectionManager(session=session).create_collection(CollectionModel(id=0, name='Default', description='Default collection'))
            await CollectionManager(session=session).create_collection(CollectionModel(id=1, name='Test collection', description='Test collection description'))
            await CollectionManager(session=session).create_collection(CollectionModel(id=2, name='Test collection 2', description='Test collection 2 description'))
        except Exception:
            print('Collection data already inserted.')

        try:
            print('Inserting publisher data...')
            await PublisherManager(session=session).create_publisher(PublisherModel(id=1, name='Test publisher', description='Test publisher description'))
            await PublisherManager(session=session).create_publisher(PublisherModel(id=2, name='Other publisher', description='This is other publisher'))
        except Exception:
            print('Publisher data already inserted.')

        try:
            print('Inserting author data...')
            await AuthorManager(session=session).create_author(AuthorModel(id=1, name="Jack Ryan", language_id='PT', country_id='BR'))
            await AuthorManager(session=session).create_author(AuthorModel(id=2, name="Jason Bourne", language_id='EN', country_id='DE'))
            await AuthorManager(session=session).create_author(AuthorModel(id=3, name='Frodo Baggins', language_id='PT', country_id='BR'))
        except Exception:
            print('Author data already inserted.')

        try:
            print('Inserting item data...')
            item = ItemModel(
                id=1,
                main_author_id=1,
                title="Test Item",
                subtitle="Test Subtitle",
                title_original="Original Title",
                subtitle_original="Original Subtitle",
                language_id='PT',
                publisher_id=1,
                serie_id=1,
                collection_id=0,
                owner_id=uuid.UUID("adf52a1e-7a19-11ed-a1eb-0242ac120002"),
                last_status_id='bought',
                last_status_date=datetime.date(2024, 7, 11),
                pages=370,
            )
            item_1 = await ItemManager(session=session).create_item(item)
        except Exception:
            print('Item data already inserted.')


if __name__ == "__main__":
    asyncio.run(insert_data())
