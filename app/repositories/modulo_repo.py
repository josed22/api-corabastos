from app.repositories.base_repo import BaseRepository


class ModuloRepository(BaseRepository):
    tabla = "modulo"
    columnas = ["nombre", "descripcion"]

    def obtener_por_rol(self, id_rol: int):
        """Módulos activos a los que tiene permiso un rol."""
        return self._consultar(
            """
            SELECT m.id, m.nombre, m.descripcion
            FROM modulo_x_rol mr JOIN modulo m ON m.id = mr.id_modulo
            WHERE mr.id_rol = %s AND mr.estado = TRUE AND m.estado = TRUE
            ORDER BY m.id;
            """,
            (id_rol,))
