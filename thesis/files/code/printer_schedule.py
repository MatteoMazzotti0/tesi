class PrinterSchedule(BaseModel):
    jobs: List[ScheduledJob]
    total_delay_minutes: int
    job_count: int
