from .database import SessionLocal, create_tables
from .models import Spot
from .utils.common import time_now  # UPDATED

def run():
    create_tables()
    db = SessionLocal()
    if not db.query(Spot).first():
        coords = [
            (44.63388, -92.62047),
            (44.63395, -92.62001),
            (44.63360, -92.62025),
            (44.63352, -92.62070),
        ]
        for lat, lon in coords:
            db.add(Spot(lat=lat, lon=lon, claimed_at=time_now()))
        db.commit()
    db.close()

if __name__ == "__main__":
    run()
