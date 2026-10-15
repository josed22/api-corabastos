from typing import Optional
from pydantic import BaseModel, Field


class Tienda(BaseModel):
    id_usuario: int
    id_pabellon: int
    nombre: str = Field(..., min_length=1, max_length=100)
    numero_local: str = Field(..., min_length=1, max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    estado: bool = True
