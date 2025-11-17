class SchedulingResult(BaseModel):
    summary: Summary
    printers: Dict[str, PrinterSchedule]
