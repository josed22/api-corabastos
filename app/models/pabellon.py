from typing import Optional
from pydantic import BaseModel, Field


class Pabellon(BaseModel):
    id_categoria: int
    nombre: str = Field(..., min_length=1, max_length=80)
    descripcion: Optional[str] = Field(None, max_length=300)
    estado: bool = True
