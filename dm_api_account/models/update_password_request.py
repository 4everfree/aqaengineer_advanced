from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class UpdatePasswordRequest(BaseModel):
    login: Optional[str] = None
    token: Optional[str] = None
    old_password: Optional[str] = Field(None, alias='oldPassword')
    new_password: Optional[str] = Field(None, alias='newPassword')

