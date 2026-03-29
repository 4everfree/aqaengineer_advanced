from __future__ import annotations

import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Rating(BaseModel):
    enabled: bool = Field(None)
    quality: int = Field(None)
    quantity: int = Field(None)

class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"

class User(BaseModel):
    login: str = Field(None)
    roles: List[UserRole] = Field(None)
    mediumPictureUrl: str = Field(None, alias="mediumPictureUrl")
    smallPictureUrl: str = Field(None, alias="smallPictureUrl")
    status: str = Field(None, alias="status")
    rating: Rating = Field(None)
    online: datetime.datetime = Field(None, alias="online")
    name: str = Field(None, alias="name")
    location: str = Field(None, alias="location")
    registration: datetime.datetime = Field(None, alias="registration")

class Metadata(BaseModel):
    email: str = Field(None, alias="email")

class UserEnvelope(BaseModel):
    resource: Optional[User] = None
    metadata: Optional[Metadata] = None
