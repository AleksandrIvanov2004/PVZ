from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.driver import DriverSchema
from project.infrastructure.postgres.models import Driver
from project.core.config import settings


class DriverRepository:
    _collection: Type[Driver] = Driver

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_drivers(
            self,
            session: AsyncSession,
    ) -> list[DriverSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.drivers;"
        drivers = await session.execute(text(query))
        return [DriverSchema.model_validate(obj=driver) for driver in drivers.mappings().all()]

    async def get_driver_by_id(
            self,
            session: AsyncSession,
            id_driver: int
    ) -> DriverSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.drivers where id = :id")

        result = await session.execute(query, {"id": id_driver})

        drivers_row = result.mappings().first()

        if drivers_row:
            return DriverSchema.model_validate(dict(drivers_row))
        return None

    async def insert_driver(
            self,
            session: AsyncSession,
            car_id: int,
            user_id: int
    ) -> DriverSchema | None:
        query = text(f"""
                INSERT INTO {settings.POSTGRES_SCHEMA}.drivers (car_id, user_id) 
                VALUES (:car_id, :user_id)
                RETURNING id, car_id, user_id
            """)
        result = await session.execute(query, {"car_id" : car_id, "user_id" : user_id})

        drivers_row = result.mappings().first()

        if drivers_row:
            return DriverSchema.model_validate(dict(drivers_row))
        return None

    async def delete_driver_by_id(
            self,
            session: AsyncSession,
            id_driver: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.drivers WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_driver})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_driver_by_id(
            self,
            session: AsyncSession,
            id_driver: int,
            car_id: int,
            user_id: int
    ) -> DriverSchema | None:
        query = text(f"""
                UPDATE {settings.POSTGRES_SCHEMA}.drivers 
                SET car_id = :car_id, user_id = :user_id
                WHERE id = :id 
                RETURNING id, car_id, user_id
            """)

        result = await session.execute(query, {"id" : id_driver, "car_id" : car_id, "user_id" : user_id})

        updated_row = result.mappings().first()

        if updated_row:
            return DriverSchema.model_validate(dict(updated_row))

        return None