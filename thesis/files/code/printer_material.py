from pydantic import BaseModel


class PrinterMaterial(BaseModel):
    id: int
    name: str
