from fastapi import APIRouter
router = APIRouter(tags=["meta"])

@router.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
