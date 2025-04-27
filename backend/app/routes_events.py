from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Event
from .schemas import EventOut
from .utils.auth import current_user

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.post("", response_model=EventOut)
def create_event(payload: EventOut, user=Depends(current_user), db: Session = Depends(get_db)):
    event = Event(**payload.dict(), organizer_id=user.id)
    db.add(event)
    db.commit(); db.refresh(event)
    return event
