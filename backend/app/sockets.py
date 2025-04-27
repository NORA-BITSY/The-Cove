import socketio
from jose import jwt, JWTError

from .config import settings
from .database import SessionLocal
from . import models

# --- CORS origins ---------------------------------------------------------
origins = [o.strip() for o in settings.FRONTEND_ORIGIN.split(',') if o]

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=origins
)
sio_app = socketio.ASGIApp(sio)

# --- in-memory viewer counters -------------------------------------------
ROOM_VIEWERS: dict[str, int] = {}
GLOBAL_VIEWERS: int = 0

# -------------------------------------------------------------------------
@sio.event
async def connect(sid, environ, auth):
    global GLOBAL_VIEWERS
    # optional JWT (sent from frontend via `auth: { token }`)
    user_id = None
    if auth and "token" in auth:
        try:
            payload = jwt.decode(
                auth["token"],
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALG],
            )
            user_id = payload.get("sub")
        except JWTError:
            pass
    await sio.save_session(sid, {"user_id": user_id})
    GLOBAL_VIEWERS += 1
    await sio.emit("global_viewers", GLOBAL_VIEWERS)

@sio.event
async def disconnect(sid):
    global GLOBAL_VIEWERS
    GLOBAL_VIEWERS = max(0, GLOBAL_VIEWERS - 1)
    await sio.emit("global_viewers", GLOBAL_VIEWERS)

# ----- per-stream rooms ---------------------------------------------------
@sio.event
async def join_stream(sid, data):
    room = f"stream_{data['stream_id']}"
    sess = await sio.get_session(sid)
    if not sess.get("user_id"):
        await sio.emit("error", {"msg": "Auth required"}, to=sid)
        return
    await sio.enter_room(sid, room)
    ROOM_VIEWERS[room] = ROOM_VIEWERS.get(room, 0) + 1
    await sio.emit("viewer_count", ROOM_VIEWERS[room], room=room)

@sio.event
async def leave_stream(sid, data):
    room = f"stream_{data['stream_id']}"
    await sio.leave_room(sid, room)
    ROOM_VIEWERS[room] = max(0, ROOM_VIEWERS.get(room, 1) - 1)
    await sio.emit("viewer_count", ROOM_VIEWERS[room], room=room)

@sio.event
async def chat_message(sid, data):
    room = f"stream_{data['stream_id']}"
    msg  = data["message"]

    sess = await sio.get_session(sid)
    db   = SessionLocal()
    user = db.query(models.User).filter_by(fb_id=sess.get("user_id")).first() if sess.get("user_id") else None
    db.close()

    await sio.emit(
        "chat_message",
        {"user": user.name if user else "Guest", "message": msg},
        room=room,
    )
