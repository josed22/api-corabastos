from app.repositories.base_repo import BaseRepository


class ProductoRepository(BaseRepository):
    tabla = "producto"
    columnas = ["id_tipo", "codigo", "nombre", "unidad_medida"]
