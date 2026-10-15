from app.core.errores import ReglaDeNegocioError
from app.repositories.base_repo import BaseRepository


class DetalleReservaRepository(BaseRepository):
    tabla = "detalle_reserva"
    columnas = ["id_reserva", "id_producto", "cantidad", "precio_unitario"]

    def crear(self, datos: dict):
        """El precio unitario se toma del precio del día; el comprador no lo envía."""
        precio = self._consultar(
            "SELECT precio FROM precio_dia WHERE id_producto = %s AND fecha = CURRENT_DATE AND estado = TRUE;",
            (datos["id_producto"],), uno=True)
        if not precio:
            raise ReglaDeNegocioError("El producto no tiene precio del día publicado")
        return super().crear({**datos, "precio_unitario": precio["precio"]})
