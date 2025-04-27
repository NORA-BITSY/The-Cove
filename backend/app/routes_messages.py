from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Message
from .schemas import MessageIn, MessageOut
from .utils.auth import current_user
from .sockets import sio
from datetime import datetime
from .middleware import limiter

router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("", response_model=list[MessageOut])
def get_recent_messages(limit: int = 50, db: Session = Depends(get_db)):
    msgs = db.query(Message).order_by(Message.timestamp.desc()).limit(limit).all()
    return list(reversed([MessageOut.from_orm(m) for m in msgs]))

@router.post("", response_model=MessageOut)
@limiter.limit("5/minute")
def post_message(data: MessageIn, db: Session = Depends(get_db), user = Depends(current_user)):
    new_msg = Message(content=data.content, author_id=user.id, timestamp=datetime.utcnow())
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    msg_out = MessageOut.from_orm(new_msg)
    sio.emit("message_new", msg_out.dict())
    return msg_out
