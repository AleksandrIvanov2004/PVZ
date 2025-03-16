from datetime import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.working_shift import WorkingShiftSchema
from project.infrastructure.postgres.models import WorkingShift
from project.core.config import settings


class WorkingShiftRepository:
    _collection: Type[WorkingShift] = WorkingShift

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_working_shifts(
            self,
            session: AsyncSession,
    ) -> list[WorkingShiftSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.working_shifts;"
        working_shifts = await session.execute(text(query))
        return [WorkingShiftSchema.model_validate(obj=working_shift) for working_shift in working_shifts.mappings().all()]

    async def get_working_shift_by_id(
            self,
            session: AsyncSession,
            id_working_shift: int
    ) -> WorkingShiftSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.working_shifts where id = :id")

        result = await session.execute(query, {"id": id_working_shift})

        working_shift_row = result.mappings().first()

        if working_shift_row:
            return WorkingShiftSchema.model_validate(dict(working_shift_row))
        return None

    async def insert_working_shift(
            self,
            session: AsyncSession,
            user_id: int,
            start_time: datetime,
            end_time: datetime
    ) -> WorkingShiftSchema | None:
        query = text(f"""
                INSERT INTO {settings.POSTGRES_SCHEMA}.working_shifts (user_id, start_time, end_time) 
                VALUES (:user_id, :start_time, :end_time)
                RETURNING id, user_id, start_time, end_time
            """)
        result = await session.execute(query, {"user_id" : user_id, "start_time" : start_time
                                                      , "end_time" : end_time})

        working_shifts_row = result.mappings().first()

        if working_shifts_row:
            return WorkingShiftSchema.model_validate(dict(working_shifts_row))
        return None

    async def delete_working_shift_by_id(
            self,
            session: AsyncSession,
            id_working_shift: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.working_shifts WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_working_shift})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_working_shift_by_id(
            self,
            session: AsyncSession,
            id_working_shift: int,
            user_id: int,
            start_time: datetime,
            end_time: datetime
    ) -> WorkingShiftSchema | None:
        query = text(f"""
                UPDATE {settings.POSTGRES_SCHEMA}.working_shifts 
                SET user_id = :user_id, start_time = :start_time, end_time = :end_time
                WHERE id = :id 
                RETURNING id, user_id, start_time, end_time
            """)

        result = await session.execute(query, {"id" : id_working_shift, "user_id" : user_id,
                                               "start_time" : start_time, "end_time" : end_time})

        updated_row = result.mappings().first()

        if updated_row:
            return WorkingShiftSchema.model_validate(dict(updated_row))

        return None