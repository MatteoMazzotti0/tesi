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
