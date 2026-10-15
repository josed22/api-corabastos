from app.repositories.base_repo import BaseRepository


class PrecioDiaRepository(BaseRepository):
    tabla = "precio_dia"
    columnas = ["id_producto", "id_usuario", "fecha", "precio"]

    def variaciones(self, fecha=None):
        return self._consultar(
            "SELECT * FROM v_variacion_precio WHERE fecha = COALESCE(%s, CURRENT_DATE) "
            "ORDER BY variacion_pct DESC NULLS LAST;",
            (fecha,))

    def historial_variacion(self, producto_id: int):
        return self._consultar(
            "SELECT * FROM v_variacion_precio WHERE id_producto = %s ORDER BY fecha DESC;",
            (producto_id,))
