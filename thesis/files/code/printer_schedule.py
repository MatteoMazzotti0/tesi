from typing import List

from pydantic import BaseModel

from .scheduled_job import ScheduledJob


class PrinterSchedule(BaseModel):
    jobs: List[ScheduledJob]
    total_delay_minutes: int
    job_count: int
