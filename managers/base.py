from typing import Any, List, Sequence, Type

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Executable

from models.base import SQLModel
from schemas.reading import ReadingSchema


class BaseDataManager:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    """Base data manager class responsible for operations over database."""

    async def add_one(self, model: SQLModel) -> SQLModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return model

    def add_all(self, models: Sequence[Any]) -> None:
        self.session.add_all(models)

    async def get_one(self, select_stmt: Executable, schema: Type[BaseModel], raise_exception: bool = False) -> BaseModel | None:
        """
            Get one register, if no row can return None or raise an exception, if more than one raise exception
        """
        entry = await self.session.scalar(select_stmt)

        if entry is not None:
            return schema.model_validate(entry)

        if raise_exception:
            # TODO: the text could be better
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No data found in {schema_name}'.format(schema_name=schema.__repr_name__))

        return None

    async def get_first(self):
        # TODO: create function to get first register in a list, maybe a param to order by
        pass

    async def get_all(self, select_stmt: Executable, schema: Type[BaseModel], raise_exception: bool = False) -> list[BaseModel] | None:
        values = await self.session.scalars(select_stmt)

        if values:
            return [schema.model_validate(i) for i in values]

        if raise_exception:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No data found in {schema_name}'.format(schema_name=schema.__repr_name__))

        return None

    def get_from_tvf(self, model: Type[SQLModel], *args: Any) -> List[Any]:
        """Query from table valued function.

        This is a wrapper function that can be used to retrieve data from
        table valued functions.

        Examples:
            from app.models.base import SQLModel

            class MyModel(SQLModel):
                __tablename__ = "function"
                __table_args__ = {"schema": "schema"}

                x: Mapped[int] = mapped_column("x", primary_key=True)
                y: Mapped[str] = mapped_column("y")
                z: Mapped[float] = mapped_column("z")

            # equivalent to "SELECT x, y, z FROM schema.function(1, 'AAA')"
            BaseDataManager(session).get_from_tvf(MyModel, 1, "AAA")
        """

        return self.get_all(self.select_from_tvf(model, *args))

    @staticmethod
    def select_from_tvf(model: Type[SQLModel], *args: Any) -> Executable:
        fn = getattr(getattr(func, model.schema()), model.table_name())
        stmt = select(fn(*args).table_valued(*model.fields()))
        return select(model).from_statement(stmt)
