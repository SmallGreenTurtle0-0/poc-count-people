from pydantic import BaseModel
from typing import Optional


class PeopleDetection(BaseModel):
    image: str
    type: Optional[str] = "base64"
