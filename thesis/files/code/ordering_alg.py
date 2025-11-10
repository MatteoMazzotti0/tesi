from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from app.models import Job, Printer, SchedulingResult


class OrderingAlg(ABC):
    @abstractmethod
    def schedule_jobs(
        self,
        jobs: List[Job],
        printers: List[Printer],
        base_datetime: datetime,
        initial_schedule: Optional[SchedulingResult] = None,
        is_last_schedule: bool = False,
        future_capacity_by_order: Optional[Dict[int, int]] = None,
    ) -> Tuple[bool, SchedulingResult]:
        pass
