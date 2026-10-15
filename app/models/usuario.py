from pydantic import BaseModel, Field


class Usuario(BaseModel):
    id_rol: int
    id_municipio: int
    id_tipo_identificacion: int
    nombre: str = Field(..., min_length=1, max_length=40)
    apellido: str = Field(..., min_length=1, max_length=40)
    correo: str = Field(..., max_length=150, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    direccion: str = Field(..., min_length=1, max_length=100)
    password_hash: str = Field(..., min_length=1, max_length=255)
    numero_identificacion: str = Field(..., min_length=1, max_length=30)
    estado: bool = True
