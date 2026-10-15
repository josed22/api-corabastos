from app.repositories.base_repo import BaseRepository


class ReservaRepository(BaseRepository):
    tabla = "reserva"
    columnas = ["id_usuario", "id_tienda", "id_estado_reserva", "codigo", "fecha_retiro", "observacion"]
