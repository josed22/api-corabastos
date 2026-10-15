from app.repositories.base_repo import BaseRepository


class ModuloXRolRepository(BaseRepository):
    tabla = "modulo_x_rol"
    columnas = ["id_rol", "id_modulo"]
