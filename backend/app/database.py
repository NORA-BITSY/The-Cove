from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import settings
from .models import Base

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

# Run only on first boot when migrations don’t exist yet
def create_tables():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
