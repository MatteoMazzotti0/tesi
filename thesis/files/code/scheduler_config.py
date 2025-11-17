@dataclass
class SchedulerConfig:
    """
    Classe che gestisce la configurazioen dello scheduler
    """

    minutes_per_day: int = int(os.getenv("MINUTES_PER_DAY", 24 * 60))
    jobs_start_time: int = int(os.getenv("JOBS_START_TIME", 9 * 60))
    jobs_end_time: int = int(os.getenv("JOBS_END_TIME", 18 * 60))
    material_change_penalty: int = int(os.getenv("MATERIAL_CHANGE_PENALTY", 100))
    late_penalty_per_minute: int = int(os.getenv("LATE_PENALTY_PER_MINUTE", 1))
    change_plate_time: int = int(os.getenv("CHANGE_PLATE_TIME", 5))
    solver_timeout: float = float(os.getenv("SOLVER_TIMEOUT", 300.0))
    log_search: bool = False
