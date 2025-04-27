from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

def add_cors(app):
    origins = [o.strip() for o in settings.FRONTEND_ORIGIN.split(',') if o]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.limiter = limiter
    app.add_exception_handler(429, _rate_limit_exceeded_handler)
