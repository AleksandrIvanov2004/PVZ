from pydantic import BaseModel, Field, ConfigDict


class DriverSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    car_id: int
    user_id: int