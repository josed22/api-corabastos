from app.core.database import Database


class BaseRepository:
    """Operaciones comunes sobre una tabla. Cada repositorio define su tabla y sus columnas."""
    tabla = ""
    columnas = []      # columnas editables (sin id, estado, creado ni actualizado)
    seleccion = "*"    # columnas que se devuelven en las consultas

    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def _conectar(self):
        conn = self.db.get_connection()
        if conn is None:
            raise ConnectionError("No fue posible conectar con la base de datos")
        return conn

    def _consultar(self, query, params=None, uno=False):
        conn = self._conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone() if uno else cursor.fetchall()
        finally:
            conn.close()

    def _modificar(self, query, params):
        conn = self._conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            fila = cursor.fetchone()
            conn.commit()
            return fila
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def obtener_todos(self, incluir_inactivos: bool = False):
        filtro = "" if incluir_inactivos else "WHERE estado = TRUE"
        return self._consultar(f"SELECT {self.seleccion} FROM {self.tabla} {filtro} ORDER BY id ASC;")

    def obtener_por_id(self, registro_id: int):
        return self._consultar(f"SELECT {self.seleccion} FROM {self.tabla} WHERE id = %s;", (registro_id,), uno=True)

    def crear(self, datos: dict):
        columnas = [c for c in self.columnas if c in datos]
        marcas = ", ".join(["%s"] * len(columnas))
        query = f"INSERT INTO {self.tabla} ({', '.join(columnas)}) VALUES ({marcas}) RETURNING id;"
        fila = self._modificar(query, [datos[c] for c in columnas])
        return fila["id"]

    def actualizar(self, registro_id: int, datos: dict):
        columnas = [c for c in self.columnas + ["estado"] if c in datos]
        asignaciones = ", ".join(f"{c} = %s" for c in columnas)
        query = f"UPDATE {self.tabla} SET {asignaciones} WHERE id = %s RETURNING id;"
        fila = self._modificar(query, [datos[c] for c in columnas] + [registro_id])
        return fila is not None

    def eliminar(self, registro_id: int):
        """Eliminado lógico: solo cambia el estado a falso."""
        query = f"UPDATE {self.tabla} SET estado = FALSE WHERE id = %s RETURNING id;"
        return self._modificar(query, (registro_id,)) is not None
