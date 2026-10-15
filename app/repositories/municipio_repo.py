from app.repositories.base_repo import BaseRepository


class MunicipioRepository(BaseRepository):
    tabla = "municipio"
    columnas = ["nombre"]
