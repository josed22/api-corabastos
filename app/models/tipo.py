from typing import Optional
from pydantic import BaseModel, Field


class Tipo(BaseModel):
    id_categoria: int
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    estado: bool = True
