from pydantic import BaseModel, Field


class Inventario(BaseModel):
    id_tienda: int
    id_producto: int
    cantidad_disponible: float = Field(0, ge=0)
    estado: bool = True
