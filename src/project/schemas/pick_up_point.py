from pydantic import BaseModel, Field, ConfigDict


class PickUpPointSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    region: int
    address: str