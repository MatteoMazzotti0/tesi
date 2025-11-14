from typing import Dict

from pydantic import BaseModel

from .responses.printer_schedule import PrinterSchedule
from .responses.summary import Summary


class SchedulingResult(BaseModel):
    summary: Summary
    printers: Dict[str, PrinterSchedule]
