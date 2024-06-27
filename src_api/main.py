import sys
import os

sys.path.append("src_api")
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from services.yolo.detect import Detector

from api.endpoints.count_people import count_people_router
from api.endpoints.health import health_router
from dotenv import load_dotenv

load_dotenv()
WEIGHT_PATH = os.getenv("WEIGHT_PATH")


@asynccontextmanager
async def detect_people(app: FastAPI):
    app.state.detector = Detector.load(WEIGHT_PATH)

    yield


app = FastAPI(lifespan=detect_people)


@app.middleware("http")
async def add_detector(request: Request, call_next):
    request.state.detector = app.state.detector
    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(count_people_router)
app.include_router(health_router)
