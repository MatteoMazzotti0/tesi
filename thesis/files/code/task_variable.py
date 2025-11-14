from dataclasses import dataclass

from ortools.sat.python.cp_model import IntervalVar, IntVar

from .job import Job


@dataclass
class TaskVariable:
    start: IntVar
    end: IntVar
    assigned: IntVar
    interval: IntervalVar
    material: str
    duration: int
    deadline: int
    job_instance: Job
