class PrinterWork(BaseModel):
    id: int
    work_name: str
    printer_material: PrinterMaterial
    plates: List[Plate]
