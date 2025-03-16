from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.user import UserSchema
from project.infrastructure.postgres.models import User
from project.core.config import settings


class UserRepository:
    _collection: Type[User] = User
    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[UserSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.users;"
        users = await session.execute(text(query))
        return [UserSchema.model_validate(obj=user) for user in users.mappings().all()]

    async def get_user_by_id(
            self,
            session: AsyncSession,
            id_user: int
    ) -> UserSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.users where id = :id")

        result = await session.execute(query, {"id": id_user})

        users_row = result.mappings().first()

        if users_row:
            return UserSchema.model_validate(dict(users_row))
        return None

    async def insert_user(
            self,
            session: AsyncSession,
            login: str,
            password: str,
            surname: str,
            name: str,
            last_name: str,
            age: int,
            phone_number: str,
            region: int
    ) -> UserSchema | None:
        query = text(f"""
                INSERT INTO {settings.POSTGRES_SCHEMA}.users (login, password, surname, name, last_name, age, phone_number, region) 
                VALUES (:login, :password, :surname, :name, :last_name, :age, :phone_number, :region)
                RETURNING id, login, password, surname, name, last_name, age, phone_number, region
            """)
        result = await session.execute(query,{"login" : login, "password" : password, "surname" : surname,
                                              "name" : name, "last_name" : last_name, "age" : age,
                                              "phone_number" : phone_number, "region" : region})

        users_row = result.mappings().first()

        if users_row:
            return UserSchema.model_validate(dict(users_row))
        return None

    async def delete_user_by_id(
            self,
            session: AsyncSession,
            id_user: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_user})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_user_by_id(
            self,
            session: AsyncSession,
            id_user: int,
            login: str,
            password: str,
            surname: str,
            name: str,
            last_name: str,
            age: int,
            phone_number: str,
            region: int
    ) -> UserSchema | None:
        query = text(f"""
                UPDATE {settings.POSTGRES_SCHEMA}.users 
                SET login = :login, password = :password, surname = :surname, name = :name, last_name = :last_name,
                 age = :age, phone_number = :phone_number, region = :region
                WHERE id = :id 
                RETURNING id, login, password, surname, name, last_name, age, phone_number, region
            """)

        result = await session.execute(query, {"id" : id_user, "login" : login, "password" : password,
                                              "surname" : surname,
                                              "name" : name, "last_name" : last_name, "age" : age,
                                              "phone_number" : phone_number, "region" : region})

        updated_row = result.mappings().first()

        if updated_row:
            return UserSchema.model_validate(dict(updated_row))

        return None