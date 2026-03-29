from pydantic import BaseModel, Field

class UserUpdatedPassword(BaseModel):
    login: str = Field(None)
    token: str = Field(None)
    oldPassword: str = Field(None)
    newPassword: str = Field(None)