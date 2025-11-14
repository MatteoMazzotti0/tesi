from typing import List

from pydantic import BaseModel

from ..order import Order
from ..printer import Printer


class ScheduleRequest(BaseModel):
    orders: List[Order]
    printers: List[Printer]
    user_id: int
    callback_token: str
