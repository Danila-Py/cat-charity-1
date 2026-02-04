from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Базовый класс для получения и создания объекта."""

    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        result = db_objs.scalars().all()
        return result

    async def create(
        self,
        obj_in,
        session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_active_objs(
        self,
        session: AsyncSession
    ):
        active_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested == false()).order_by(
                    self.model.id)
        )
        return active_objs.scalars().all()