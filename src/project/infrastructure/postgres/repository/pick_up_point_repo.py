from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.pick_up_point import PickUpPointSchema
from project.infrastructure.postgres.models import PickUpPoint
from project.core.config import settings


class PickUpPointRepository:
    _collection: Type[PickUpPoint] = PickUpPoint

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_pick_up_points(
            self,
            session: AsyncSession,
    ) -> list[PickUpPointSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.pick_up_points;"
        pick_up_points = await session.execute(text(query))
        return [PickUpPointSchema.model_validate(obj=pick_up_point) for pick_up_point in pick_up_points.mappings().all()]

    async def get_pick_up_point_by_id(
            self,
            session: AsyncSession,
            id_pick_up_point: int
    ) -> PickUpPointSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.pick_up_points where id = :id")

        result = await session.execute(query, {"id": id_pick_up_point})

        pick_up_points_row = result.mappings().first()

        if pick_up_points_row:
            return PickUpPointSchema.model_validate(dict(pick_up_points_row))
        return None

    async def insert_pick_up_point(
            self,
            session: AsyncSession,
            region: int,
            address: str
    ) -> PickUpPointSchema | None:
        query = text(f"""
                INSERT INTO {settings.POSTGRES_SCHEMA}.pick_up_points (region, address) 
                VALUES (:region, :address)
                RETURNING id, region, address
            """)
        result = await session.execute(query, {"region" : region, "address" : address})

        pick_up_points_row = result.mappings().first()

        if pick_up_points_row:
            return PickUpPointSchema.model_validate(dict(pick_up_points_row))
        return None

    async def delete_pick_up_point_by_id(
            self,
            session: AsyncSession,
            id_pick_up_point: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.pick_up_points WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_pick_up_point})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_pick_up_point_by_id(
            self,
            session: AsyncSession,
            id_pick_up_point: int,
            region: int,
            address: str
    ) -> PickUpPointSchema | None:
        query = text(f"""
                UPDATE {settings.POSTGRES_SCHEMA}.pick_up_points 
                SET region = :region, address = :address
                WHERE id = :id 
                RETURNING id, region, address
            """)

        result = await session.execute(query, {"id" : id_pick_up_point, "region" : region, "address" : address})

        updated_row = result.mappings().first()

        if updated_row:
            return PickUpPointSchema.model_validate(dict(updated_row))

        return None