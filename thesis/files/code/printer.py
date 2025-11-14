from pydantic import BaseModel


class Printer(BaseModel):
    id: int
    name: str
