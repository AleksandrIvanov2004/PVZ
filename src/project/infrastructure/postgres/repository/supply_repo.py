from datetime import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.supply import SupplySchema
from project.infrastructure.postgres.models import Supply
from project.core.config import settings



class SupplyRepository:
    _collection: Type[Supply] = Supply

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_supplies(
            self,
            session: AsyncSession,
    ) -> list[SupplySchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.supplies;"
        supplies = await session.execute(text(query))
        return [SupplySchema.model_validate(obj=supply) for supply in supplies.mappings().all()]

    async def get_supply_by_id(
            self,
            session: AsyncSession,
            id_supply: int
    ) -> SupplySchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.supplies where id = :id")

        result = await session.execute(query, {"id": id_supply})

        supplies_row = result.mappings().first()

        if supplies_row:
            return SupplySchema.model_validate(dict(supplies_row))
        return None

    async def insert_supply(
            self,
            session: AsyncSession,
            car_number: str,
            pick_up_point_id: int,
            time: datetime
    ) -> SupplySchema | None:
        query = text(f"""
                INSERT INTO {settings.POSTGRES_SCHEMA}.supplies (car_number, pick_up_point_id, time) 
                VALUES (:car_number, :pick_up_point_id, :time)
                RETURNING id, car_number, pick_up_point_id, time
            """)
        result = await session.execute(query, {"car_number" : car_number, "pick_up_point_id" : pick_up_point_id,
                                               "time" : time})

        supplies_row = result.mappings().first()

        if supplies_row:
            return SupplySchema.model_validate(dict(supplies_row))
        return None

    async def delete_supply_by_id(
            self,
            session: AsyncSession,
            id_supply: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.supplies WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_supply})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_supply_by_id(
            self,
            session: AsyncSession,
            id_supply: int,
            car_number: str,
            pick_up_point_id: int,
            time: datetime
    ) -> SupplySchema | None:
        query = text(f"""
                UPDATE {settings.POSTGRES_SCHEMA}.supplies 
                SET car_number = :car_number, pick_up_point_id = :pick_up_point_id, time = :time
                WHERE id = :id 
                RETURNING id, car_number, pick_up_point_id, time
            """)

        result = await session.execute(query, {"id" : id_supply, "car_number" : car_number,
                                               "pick_up_point_id" : pick_up_point_id, "time" : time})

        updated_row = result.mappings().first()

        if updated_row:
            return SupplySchema.model_validate(dict(updated_row))

        return None