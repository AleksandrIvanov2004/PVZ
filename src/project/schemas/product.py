from pydantic import BaseModel, Field, ConfigDict

from project.infrastructure.postgres.models import StatusEnum_1


class ProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    supply_id: int
    status: StatusEnum_1