# schemas/player.py — Pydantic models for request validation and response shape

from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


# ── What frontend SENDS when adding a player ─────────────────────────────
class PlayerInput(BaseModel):
    username: str = Field(...,min_length=3,max_length=10)
    score: int = Field(...,ge=0,le=1000)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not value.isalnum():
            raise ValueError(
                "Username must contain only letters and numbers"
            )
        return value


# ── What the API RETURNS to the frontend ─────────────────────────────────
class PlayerResponse(BaseModel):
    id:         int
    username:   str
    score:      int
    created_at: datetime

    class Config:
        from_attributes = True  # allows converting SQLAlchemy model → this schema

