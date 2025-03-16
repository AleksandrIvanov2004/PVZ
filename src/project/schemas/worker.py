from pydantic import BaseModel, Field, ConfigDict


class WorkerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    pick_up_point_id: int