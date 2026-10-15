from app.repositories.base_repo import BaseRepository


class TipoRepository(BaseRepository):
    tabla = "tipo"
    columnas = ["id_categoria", "nombre", "descripcion"]
