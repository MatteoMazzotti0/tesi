class Order(BaseModel):
    id: int
    expiration_date: date
    number: str
    pcs_ordered: int
    pcs_printed: int
    printer_work: PrinterWork
