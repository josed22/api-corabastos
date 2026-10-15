from app.repositories.base_repo import BaseRepository


class TiendaRepository(BaseRepository):
    tabla = "tienda"
    columnas = ["id_usuario", "id_pabellon", "nombre", "numero_local", "telefono"]
