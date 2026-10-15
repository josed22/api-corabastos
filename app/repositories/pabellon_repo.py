from app.repositories.base_repo import BaseRepository


class PabellonRepository(BaseRepository):
    tabla = "pabellon"
    columnas = ["id_categoria", "nombre", "descripcion"]
