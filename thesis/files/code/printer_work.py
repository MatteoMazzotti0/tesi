from typing import List

from pydantic import BaseModel

from .plate import Plate
from .printer_material import PrinterMaterial


class PrinterWork(BaseModel):
    id: int
    work_name: str
    printer_material: PrinterMaterial
    plates: List[Plate]
