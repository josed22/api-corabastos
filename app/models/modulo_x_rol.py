from pydantic import BaseModel, Field


class ModuloXRol(BaseModel):
    id_rol: int
    id_modulo: int
    estado: bool = True
