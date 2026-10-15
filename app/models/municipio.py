from pydantic import BaseModel, Field


class Municipio(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=80)
    estado: bool = True
