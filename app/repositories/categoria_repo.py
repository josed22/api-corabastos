from app.repositories.base_repo import BaseRepository


class CategoriaRepository(BaseRepository):
    tabla = "categoria"
    columnas = ["nombre", "descripcion"]
