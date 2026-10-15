from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class Reserva(BaseModel):
    id_usuario: Optional[int] = None
    id_tienda: int
    id_estado_reserva: int
    codigo: str = Field(..., min_length=1, max_length=30)
    fecha_retiro: date
    observacion: Optional[str] = Field(None, max_length=300)
    estado: bool = True
