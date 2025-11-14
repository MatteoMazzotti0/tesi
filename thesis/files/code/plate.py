from datetime import time

from pydantic import BaseModel


class Plate(BaseModel):
    id: int
    pcs: int
    time: time
