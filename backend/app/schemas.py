from pydantic import BaseModel, Field
from datetime import datetime

# ---------- Auth ----------
class FBLogin(BaseModel):
    access_token: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- Spot ----------
class SpotOut(BaseModel):
    id: int
    lat: float
    lon: float
    note: str | None = None
    claimed_at: datetime | None = None
    checked_in: bool
    claimant_id: int | None = None

    class Config: 
        orm_mode = True

# ---------- Event ----------
class EventOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    location: str | None = None
    organizer_id: int

    class Config:
        orm_mode = True

# ---------- Alert ----------
class AlertOut(BaseModel):
    id: int
    alert_type: str
    description: str | None = None
    lat: float | None = None
    lon: float | None = None
    created_at: datetime
    reporter_id: int

    class Config:
        orm_mode = True

class StreamCreate(BaseModel):
    title: str

class StreamOut(BaseModel):
    id: str
    title: str
    active: bool
    created_at: datetime
    streamer_name: str

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            title=obj.title,
            active=obj.active,
            created_at=obj.created_at,
            streamer_name=obj.streamer.name if obj.streamer else "Unknown",
        )

    model_config = {"orm_mode": True}

# ---------- Messages ----------
class MessageIn(BaseModel):
    content: str = Field(..., max_length=280)

class MessageOut(BaseModel):
    id: int
    content: str
    author_id: int | None
    timestamp: datetime
    class Config:
        orm_mode = True

# ---------- Reviews ----------
class ReviewIn(BaseModel):
    business_name: str
    rating: int
    comment: str | None = None

class ReviewOut(BaseModel):
    id: int
    business_name: str
    rating: int
    comment: str | None = None
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True

# ---------- Badges ----------
class BadgesOut(BaseModel):
    badges: list[str]
