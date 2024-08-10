import asyncio

from rolf_common.managers import BaseDataManager

from backend.database import db_session, sessionmanager
from managers.core import LanguageManager, CountryManager, SerieManager
from models import StatusModel, LanguageModel, CountryModel, SerieModel


async def insert_data():
    async with sessionmanager.session() as session:
        print('Inserting item status data...')
        await BaseDataManager(session=session).add_one(StatusModel(id='owned', name='Na estante', type='ITEM.STATUS'))
        await BaseDataManager(session=session).add_one(StatusModel(id='bought', name='Comprado', type='ITEM.STATUS'))
        await BaseDataManager(session=session).add_one(StatusModel(id='desired', name='Desejado', type='ITEM.STATUS'))

        print('Inserting reading status data...')
        await BaseDataManager(session=session).add_one(StatusModel(id='reading', name='Lendo', type='READING.STATUS'))
        await BaseDataManager(session=session).add_one(StatusModel(id='read', name='Lido', type='READING.STATUS'))

        print('Inserting language data...')
        await LanguageManager(session=session).create_language(LanguageModel(id='EN', name='English', code='EN'))
        await LanguageManager(session=session).create_language(LanguageModel(id='PT', name='Portuguese', code='PT'))

        print('Inserting country data...')
        await CountryManager(session=session).create_country(CountryModel(id='BR', name='Brasil', continent='SA'))
        await CountryManager(session=session).create_country(CountryModel(id='DE', name='Alemanha', continent='EU'))
        await CountryManager(session=session).create_country(CountryModel(id='AU', name='Austrália', continent='OC'))

        print('Inserting serie data...')
        await SerieManager(session=session).create_serie(SerieModel(id=0, name='Default', description='Default serie'))
        await SerieManager(session=session).create_serie(SerieModel(id=1, name='Test serie', description='Test serie description'))
        await SerieManager(session=session).create_serie(SerieModel(id=2, name='Test serie 2', description='Test serie 2 description'))


if __name__ == "__main__":
    asyncio.run(insert_data())
