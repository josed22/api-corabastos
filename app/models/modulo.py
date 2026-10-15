from typing import Optional
from pydantic import BaseModel, Field


class Modulo(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = None
    estado: bool = True
