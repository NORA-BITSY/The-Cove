from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Alert
from .schemas import AlertOut
from .utils.auth import current_user
from .middleware import limiter

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("", response_model=list[AlertOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.created_at.desc()).all()

@router.post("", response_model=AlertOut)
@limiter.limit("30/minute")
def create_alert(alert: AlertOut, user=Depends(current_user), db: Session = Depends(get_db)):
    new = Alert(**alert.dict(exclude={"id", "created_at"}), reporter_id=user.id)
    db.add(new); db.commit(); db.refresh(new)
    from .sockets import sio
    sio.emit("alert_new", AlertOut.model_validate(new).model_dump())
    return new
