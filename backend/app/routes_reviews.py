from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Review
from .schemas import ReviewIn, ReviewOut
from .utils.auth import current_user
from datetime import datetime

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("", response_model=list[ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@router.post("", response_model=ReviewOut)
def create_review(data: ReviewIn, db: Session = Depends(get_db), user = Depends(current_user)):
    new_review = Review(
        business_name = data.business_name,
        rating = data.rating,
        comment = data.comment,
        user_id = user.id,
        created_at = datetime.utcnow()
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return ReviewOut.from_orm(new_review)
