from pydantic import BaseModel, Field, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    password: str
    surname: str
    name: str
    last_name: str
    age: int
    phone_number: str | None = Field(default=None, pattern=r"^\+?7\d{10}$", examples=["+79999999999"])
    region: int
    role: str