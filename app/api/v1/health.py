from fastapi import APIRouter
import time


router = APIRouter(tags=["health"])


@router.get("/health", summary="Health check")
def health():
    return {"status": "ok", "timestamp": int(time.time())}


