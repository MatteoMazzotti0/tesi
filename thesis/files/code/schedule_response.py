class ScheduleResponse(BaseModel):
    result: SchedulingResult
    orders: List[Order]
    user_id: int

