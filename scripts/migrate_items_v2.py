import asyncio
from managers.item import ItemManager
from backend.database import sessionmanager


async def fetch_items():
    async with sessionmanager.session() as session:
        item_manager = ItemManager(session)

        items = await item_manager.get_items()
        print(items)
        return items


async def main():
    await fetch_items()


if __name__ == "__main__":
    asyncio.run(main())
