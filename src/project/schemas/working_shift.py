from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class WorkingShiftSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    worker_id: int
    start_time: datetime
    end_time: datetime