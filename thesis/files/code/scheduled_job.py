from datetime import datetime

from pydantic import BaseModel

from ..order import Order
from ..plate import Plate


class ScheduledJob(BaseModel):
    job_name: str
    material: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    delay_minutes: int
    order: Order
    deadline: datetime
    plate: Plate
