from pydantic import BaseModel, Field


class EstadoReserva(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=40)
    estado: bool = True
