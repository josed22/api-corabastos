from app.repositories.base_repo import BaseRepository


class UsuarioRepository(BaseRepository):
    tabla = "usuario"
    columnas = ["id_rol", "id_municipio", "id_tipo_identificacion", "nombre", "apellido", "correo", "direccion", "password_hash", "numero_identificacion"]

    seleccion = ("id, id_rol, id_municipio, id_tipo_identificacion, nombre, apellido, correo, "
                 "direccion, numero_identificacion, estado, creado, actualizado")  # nunca devuelve la contraseña

    def obtener_por_correo(self, correo: str):
        """Usuario activo con su rol, usado para el login."""
        return self._consultar(
            """
            SELECT u.id, u.id_rol, u.nombre, u.apellido, u.correo, u.password_hash, r.nombre AS rol
            FROM usuario u JOIN rol r ON r.id = u.id_rol
            WHERE u.correo = %s AND u.estado = TRUE AND r.estado = TRUE;
            """,
            (correo,), uno=True)

    def obtener_activo_con_rol(self, usuario_id: int):
        """Usuario activo con su rol, usado para validar el token."""
        return self._consultar(
            """
            SELECT u.id, u.id_rol, u.nombre, u.apellido, u.correo, r.nombre AS rol
            FROM usuario u JOIN rol r ON r.id = u.id_rol
            WHERE u.id = %s AND u.estado = TRUE AND r.estado = TRUE;
            """,
            (usuario_id,), uno=True)
