from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health")
def get_health():
    return {"status": "ok"}
