from app.repositories.base_repo import BaseRepository


class EstadoReservaRepository(BaseRepository):
    tabla = "estado_reserva"
    columnas = ["nombre"]
