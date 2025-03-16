from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.car import CarSchema
from project.infrastructure.postgres.models import Car
from project.core.config import settings


class CarRepository:
    _collection: Type[Car] = Car

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_cars(
        self,
        session: AsyncSession,
    ) -> list[CarSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.cars;"
        cars = await session.execute(text(query))
        return [CarSchema.model_validate(obj=car) for car in cars.mappings().all()]

    async def get_car_by_id(
            self,
            session: AsyncSession,
            id_car: int
    ) -> CarSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.cars where id = :id")

        result = await session.execute(query, {"id": id_car})

        cars_row = result.mappings().first()

        if cars_row:
            return CarSchema.model_validate(dict(cars_row))
        return None

    async def insert_car(
            self,
            session: AsyncSession,
            number: str,
            region: int
    ) -> CarSchema | None:
        query = text(f"""
                INSERT INTO {settings.POSTGRES_SCHEMA}.cars (number, region) 
                VALUES (:number, :region)
                RETURNING number, region
            """)
        result = await session.execute(query,{"number" : number, "region" : region})

        cars_row = result.mappings().first()

        if cars_row:
            return CarSchema.model_validate(dict(cars_row))
        return None

    async def delete_car_by_id(
            self,
            session: AsyncSession,
            id_car: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.cars WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_car})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_car_by_id(
            self,
            session: AsyncSession,
            id_car: int,
            number: str,
            region: int
    ) -> CarSchema | None:
        query = text(f"""
                UPDATE {settings.POSTGRES_SCHEMA}.cars 
                SET number = :number, region = :region
                WHERE id = :id 
                RETURNING id, number, region
            """)

        result = await session.execute(query, {"id" : id_car, "number" : number, "region" : region})

        updated_row = result.mappings().first()

        if updated_row:
            return CarSchema.model_validate(dict(updated_row))

        return None

