from fastapi import FastAPI
from .middleware import add_cors
from .routes import api_router
from .sockets import sio_app
from .seed import run as seed_db

app = FastAPI(title="The Cove API", version="0.4.0")
add_cors(app)
seed_db()

# Prometheus AFTER app exists
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

# Sentry AFTER everything else (optional)
import os, sentry_sdk
if (dsn := os.getenv("SENTRY_DSN")):
    sentry_sdk.init(dsn=dsn, traces_sample_rate=0.2)

app.include_router(api_router)
app.mount("/ws", sio_app)
