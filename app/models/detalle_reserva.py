from pydantic import BaseModel, Field


class DetalleReserva(BaseModel):
    id_reserva: int
    id_producto: int
    cantidad: float = Field(..., gt=0)
    estado: bool = True
