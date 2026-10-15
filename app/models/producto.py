from pydantic import BaseModel, Field


class Producto(BaseModel):
    id_tipo: int
    codigo: str = Field(..., min_length=1, max_length=30)
    nombre: str = Field(..., min_length=1, max_length=100)
    unidad_medida: str = Field("kg", min_length=1, max_length=20)
    estado: bool = True
