from app.repositories.base_repo import BaseRepository


class RolRepository(BaseRepository):
    tabla = "rol"
    columnas = ["nombre"]
