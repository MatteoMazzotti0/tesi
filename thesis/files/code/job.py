from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel

from .order import Order
from .plate import Plate


class Job(BaseModel):
    name: str
    time: time
    material: str
    plate: Plate
    end_time: datetime
    order: Order
