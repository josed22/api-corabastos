from app.core.errores import ReglaDeNegocioError
from app.repositories.base_repo import BaseRepository


class InventarioRepository(BaseRepository):
    tabla = "inventario"
    columnas = ["id_tienda", "id_producto", "cantidad_disponible"]

    def _validar_categoria(self, datos: dict):
        """Una tienda solo puede tener productos de la categoría de su pabellón."""
        fila = self._consultar(
            """
            SELECT 1
            FROM tienda ti
            JOIN pabellon pa ON pa.id = ti.id_pabellon
            JOIN producto p  ON p.id = %s
            JOIN tipo t      ON t.id = p.id_tipo
            WHERE ti.id = %s AND t.id_categoria = pa.id_categoria;
            """,
            (datos["id_producto"], datos["id_tienda"]), uno=True)
        if not fila:
            raise ReglaDeNegocioError(
                "El producto no pertenece a la categoría del pabellón de la tienda (o la tienda/producto no existe)")

    def crear(self, datos: dict):
        self._validar_categoria(datos)
        return super().crear(datos)

    def actualizar(self, registro_id: int, datos: dict):
        self._validar_categoria(datos)
        return super().actualizar(registro_id, datos)
