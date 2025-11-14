from typing import List, Self

from pydantic import BaseModel

from ..order import Order
from ..scheduling_result import SchedulingResult


class ScheduleResponse(BaseModel):
    result: SchedulingResult
    orders: List[Order]
    user_id: int

