from pydantic import BaseModel, ConfigDict


class LoginSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    password: str