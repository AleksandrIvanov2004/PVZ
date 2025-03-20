from pydantic import BaseModel, Field, ConfigDict


class CarSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str | None = Field(
        default=None,
        pattern=r"^[А-Я]{1}\d{3}[А-Я]{2}$",
        examples=["А123ВС"]
    )
    region: int