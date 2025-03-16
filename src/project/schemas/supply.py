from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class SupplySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    driver_id: int
    pick_up_point_id: int
    time: datetime