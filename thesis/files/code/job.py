class Job(BaseModel):
    name: str
    time: time
    material: str
    plate: Plate
    end_time: datetime
    order: Order
