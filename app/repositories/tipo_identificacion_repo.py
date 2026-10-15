from app.repositories.base_repo import BaseRepository


class TipoIdentificacionRepository(BaseRepository):
    tabla = "tipo_identificacion"
    columnas = ["nombre"]
