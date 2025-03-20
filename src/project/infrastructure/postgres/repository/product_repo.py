from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.product import ProductSchema
from project.infrastructure.postgres.models import Product
from project.core.config import settings

from project.infrastructure.postgres.models import StatusEnum_1


class ProductRepository:
    _collection: Type[Product] = Product

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_products(
            self,
            session: AsyncSession,
    ) -> list[ProductSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.products;"
        products = await session.execute(text(query))
        return [ProductSchema.model_validate(obj=product) for product in products.mappings().all()]

    async def get_product_by_id(
            self,
            session: AsyncSession,
            id_product: int
    ) -> ProductSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.products where id = :id")

        result = await session.execute(query, {"id": id_product})

        products_row = result.mappings().first()

        if products_row:
            return ProductSchema.model_validate(dict(products_row))
        return None

    async def insert_product(
            self,
            session: AsyncSession,
            supply_id: int,
            status: StatusEnum_1
    ) -> ProductSchema | None:
        query = text(f"""
                INSERT INTO {settings.POSTGRES_SCHEMA}.products (supply_id, status) 
                VALUES (:supply_id, :status)
                RETURNING id, supply_id, status
            """)
        result = await session.execute(query, {"supply_id" : supply_id, "status" : status})

        products_row = result.mappings().first()

        if products_row:
            return ProductSchema.model_validate(dict(products_row))
        return None

    async def delete_product_by_id(
            self,
            session: AsyncSession,
            id_product: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.products WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_product})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_product_by_id(
            self,
            session: AsyncSession,
            id_product: int,
            supply_id: int,
            status: StatusEnum_1
    ) -> ProductSchema | None:
        query = text(f"""
                UPDATE {settings.POSTGRES_SCHEMA}.products 
                SET supply_id = :supply_id, status = :status
                WHERE id = :id 
                RETURNING id, supply_id, status
            """)

        result = await session.execute(query, {"id" : id_product, "supply_id" : supply_id, "status" : status})

        updated_row = result.mappings().first()

        if updated_row:
            return ProductSchema.model_validate(dict(updated_row))

        return None