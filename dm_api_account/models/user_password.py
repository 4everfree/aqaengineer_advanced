from pydantic import BaseModel, Field


class UserPassword(BaseModel):
    login: str = Field(None)
    email: str = Field(None)
