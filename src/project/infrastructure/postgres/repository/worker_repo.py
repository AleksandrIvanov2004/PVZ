from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.worker import WorkerSchema
from project.infrastructure.postgres.models import Worker
from project.core.config import settings


class WorkerRepository:
    _collection: Type[Worker] = Worker

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_workers(
            self,
            session: AsyncSession,
    ) -> list[WorkerSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.workers;"
        workers = await session.execute(text(query))
        return [WorkerSchema.model_validate(obj=worker) for worker in workers.mappings().all()]

    async def get_worker_by_id(
            self,
            session: AsyncSession,
            id_worker: int
    ) -> WorkerSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.workers where id = :id")

        result = await session.execute(query, {"id": id_worker})

        workers_row = result.mappings().first()

        if workers_row:
            return WorkerSchema.model_validate(dict(workers_row))
        return None

    async def insert_worker(
            self,
            session: AsyncSession,
            user_id: int,
            pick_up_point_id: int
    ) -> WorkerSchema | None:
        query = text(f"""
                INSERT INTO {settings.POSTGRES_SCHEMA}.workers (user_id, pick_up_point_id) 
                VALUES (:user_id, :pick_up_point_id)
                RETURNING id, user_id, pick_up_point_id
            """)
        result = await session.execute(query, {"user_id" : user_id, "pick_up_point_id" : pick_up_point_id})

        workers_row = result.mappings().first()

        if workers_row:
            return WorkerSchema.model_validate(dict(workers_row))
        return None

    async def delete_worker_by_id(
            self,
            session: AsyncSession,
            id_worker: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.workers WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_worker})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_worker_by_id(
            self,
            session: AsyncSession,
            id_worker: int,
            user_id: int,
            pick_up_point_id: int
    ) -> WorkerSchema | None:
        query = text(f"""
                UPDATE {settings.POSTGRES_SCHEMA}.workers 
                SET user_id = :user_id, pick_up_point_id = :pick_up_point_id
                WHERE id = :id 
                RETURNING id, user_id, pick_up_point_id
            """)

        result = await session.execute(query, {"id" : id_worker, "user_id" : user_id, "pick_up_point_id" : pick_up_point_id})

        updated_row = result.mappings().first()

        if updated_row:
            return WorkerSchema.model_validate(dict(updated_row))

        return None