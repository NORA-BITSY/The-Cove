from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from . import models, schemas, utils
from .database import get_db
from .routes_events import router as events_router
from .routes_alerts import router as alerts_router
from .routes_messages import router as messages_router  # NEW
from .routes_reviews import router as reviews_router    # NEW
from .routes_badges import router as badges_router      # NEW
from .sockets import sio  # added for stream_webhook()
from .routes_health import router as health_router  # import health routes
from .middleware import limiter

api_router = APIRouter(prefix="/api", tags=["api"])


@api_router.post("/auth/facebook", response_model=schemas.Token)
def fb_login(token: schemas.FBLogin, db: Session = Depends(get_db)):
    fb_profile = utils.fb.verify_token(token.access_token)
    if not fb_profile:
        raise HTTPException(status_code=400, detail="Invalid FB token")
    user = utils.fb.upsert_user(db, fb_profile)
    return utils.fb.issue_jwt(user)


@api_router.get("/spots", response_model=list[schemas.SpotOut])
def list_spots(db: Session = Depends(get_db)):
    return db.query(models.Spot).all()


@api_router.post("/spots/{spot_id}/claim", response_model=schemas.SpotOut)
@limiter.limit("30/minute")
def claim_spot(spot_id: int, note: str | None = None,
               user=Depends(utils.auth.current_user),
               db: Session = Depends(get_db)):
    spot = db.get(models.Spot, spot_id)
    if not spot:
        raise HTTPException(404, "Spot not found")
    if spot.claimant_id:
        raise HTTPException(400, "Spot already claimed")
    spot.claimant_id = user.id
    spot.note = note
    db.commit()
    sio.emit("spot_update", {"id": spot_id, "claimed_by": user.name})
    return spot


@api_router.get("/streams", response_model=list[schemas.StreamOut])
def list_streams(db: Session = Depends(get_db)):
    q = (db.query(models.Stream)
            .join(models.User, models.Stream.user_id == models.User.id)
            .filter(models.Stream.active.is_(True))
            .options(selectinload(models.Stream.streamer)))
    return [schemas.StreamOut.from_orm(s) for s in q.all()]


@api_router.post("/streams", response_model=schemas.StreamOut)
def create_stream(payload: schemas.StreamCreate, user=Depends(utils.auth.current_user), db: Session = Depends(get_db)):
    import uuid
    stream_id = str(uuid.uuid4())
    stream = models.Stream(id=stream_id, title=payload.title, user_id=user.id, active=False)
    db.add(stream)
    db.commit()
    db.refresh(stream)
    return stream


@api_router.post("/streams/webhook")
async def stream_webhook(payload: dict, db: Session = Depends(get_db)):
    stream_id = payload.get("stream_id")
    event = payload.get("event")
    stream = db.query(models.Stream).get(stream_id)
    if not stream:
        raise HTTPException(404, "Stream not found")
    if event == "started":
        stream.active = True
        await sio.emit("stream_started", schemas.StreamOut.from_orm(stream).dict())
    elif event == "stopped":
        stream.active = False
        await sio.emit("stream_stopped", {"stream_id": stream_id})
    db.commit()
    return {"status": "ok"}

# Include sub-routers
api_router.include_router(events_router)
api_router.include_router(alerts_router)
api_router.include_router(messages_router)
api_router.include_router(reviews_router)
api_router.include_router(badges_router)
api_router.include_router(health_router)  # include /api/health