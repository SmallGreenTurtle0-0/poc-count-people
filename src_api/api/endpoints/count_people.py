import base64
from fastapi import APIRouter, Request
from schemas import PeopleDetection
from services.yolo.detect import Detector
import io
from PIL import Image

count_people_router = APIRouter(prefix="/people")


@count_people_router.get("/health")
async def health():
    return {"status": "ok"}


@count_people_router.post("/count")
async def count_people(request: Request, image: PeopleDetection) -> dict:
    detect_people: Detector = request.state.detector

    if image.type == "base64":
        image_b64 = image.image
        image_bytes = base64.b64decode(image_b64.encode("utf-8"))
        image = Image.open(io.BytesIO(image_bytes))
    else:
        image = image.image

    result = detect_people.detect(image, classes=[0], conf=0.2)[0]
    return {"people_count": len(result), "detail": result.tojson()}
