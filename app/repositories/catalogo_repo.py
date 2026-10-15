from app.repositories.base_repo import BaseRepository


class CatalogoRepository(BaseRepository):
    """Consulta de solo lectura: qué tienda tiene cada producto hoy, a qué precio y cuánto varió."""

    def buscar(self, producto=None, categoria=None):
        return self._consultar(
            """
            SELECT * FROM v_catalogo_hoy
            WHERE (%s::text IS NULL OR producto ILIKE %s)
              AND (%s::text IS NULL OR categoria ILIKE %s)
            ORDER BY producto, precio_hoy;
            """,
            (producto, f"%{producto}%" if producto else None,
             categoria, f"%{categoria}%" if categoria else None))
