from pydantic import BaseModel, Field, ConfigDict

class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="login name")
    password: str = Field(..., description="Password")
    email: str = Field(..., description="Email")