import httpx
from .auth import create_access_token
from ..models import User
from ..config import settings

GRAPH_URL = "https://graph.facebook.com/me?fields=id,name,email&access_token="

def verify_token(token: str) -> dict | None:
    try:
        r = httpx.get(GRAPH_URL + token, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def upsert_user(db, fb_profile: dict) -> User:
    user = db.query(User).filter_by(fb_id=fb_profile["id"]).first()
    if not user:
        user = User(
            fb_id=fb_profile["id"],
            name=fb_profile.get("name"),
            email=fb_profile.get("email"),
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    return user

def issue_jwt(user: User) -> dict:
    token = create_access_token({"sub": user.fb_id})
    return {"access_token": token, "token_type": "bearer"}
