from pydantic import BaseModel, Field


class TipoIdentificacion(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=60)
    estado: bool = True
