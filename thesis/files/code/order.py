from datetime import date
from math import ceil

from pydantic import BaseModel

from .plate import Plate
from .printer_work import PrinterWork


class Order(BaseModel):
    id: int
    expiration_date: date
    number: str
    pcs_ordered: int
    pcs_printed: int
    printer_work: PrinterWork
