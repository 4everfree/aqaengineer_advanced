from pydantic import BaseModel, Field

class LoginCredentials(BaseModel):
    login: str = Field(..., description='Login name')
    password: str = Field(..., description='Password')
    remember_me: bool = Field(None, description='Boolean to save cookies', serialization_alias='rememberMe')