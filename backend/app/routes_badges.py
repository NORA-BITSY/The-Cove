from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .schemas import BadgesOut
from .utils.auth import current_user

router = APIRouter(prefix="/badges", tags=["badges"])

@router.get("", response_model=BadgesOut)
def get_my_badges(db: Session = Depends(get_db), user = Depends(current_user)):
    raw = user.badges or ""
    badge_list = [b.strip() for b in raw.split(",") if b.strip()]
    return BadgesOut(badges=badge_list)

@router.post("/add", response_model=BadgesOut)
def add_badge(badge_name: str, db: Session = Depends(get_db), user = Depends(current_user)):
    existing = user.badges or ""
    if badge_name not in existing:
        updated = existing + ("," if existing else "") + badge_name
        user.badges = updated
        db.commit()
    raw = user.badges or ""
    badge_list = [b.strip() for b in raw.split(",") if b.strip()]
    return BadgesOut(badges=badge_list)
