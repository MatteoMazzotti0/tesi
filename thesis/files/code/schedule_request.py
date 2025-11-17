class ScheduleRequest(BaseModel):
    orders: List[Order]
    printers: List[Printer]
    user_id: int
    callback_token: str
