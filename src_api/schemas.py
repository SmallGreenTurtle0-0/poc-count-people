from pydantic import BaseModel
from typing import Union


class PeopleDetection(BaseModel):
    image: Union[str, bytes]
