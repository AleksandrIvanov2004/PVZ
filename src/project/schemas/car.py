from pydantic import BaseModel, Field, ConfigDict


class CarSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    region: int