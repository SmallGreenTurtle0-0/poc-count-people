from fastapi import APIRouter, Request
from schemas import PeopleDetection
from services.yolo.detect import DetectPeople


count_people_router = APIRouter(prefix="/people")


@count_people_router.get("/health")
async def health():
    return {"status": "ok"}


@count_people_router.post("/count")
async def count_people(request: Request, image: PeopleDetection):
    detect_people: DetectPeople = request.state.detector
    result = detect_people.detect(image.image)[0]
    plot_result = result.plot(
        save=True,
        filename="/home/hahoang/Desktop/Upwork/poc-count-people/data/people_count.png",
    )
    return {
        "plot": plot_result.tolist(),
        "people_count": len(result),
    }
