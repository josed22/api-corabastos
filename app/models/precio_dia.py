from datetime import date
from pydantic import BaseModel, Field


class PrecioDia(BaseModel):
    id_producto: int
    fecha: date = Field(default_factory=date.today)
    precio: float = Field(..., gt=0)
    estado: bool = True
