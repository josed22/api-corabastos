from typing import Optional

from fastapi import APIRouter, Depends

from app.api.dependencias import obtener_usuario_actual
from app.repositories.catalogo_repo import CatalogoRepository

router = APIRouter(prefix="/catalogo", tags=["Catálogo"])
repo = CatalogoRepository()


@router.get("/")
def buscar_productos(producto: Optional[str] = None, categoria: Optional[str] = None,
                     actual: dict = Depends(obtener_usuario_actual)):
    """Tiendas que tienen un producto hoy, con el precio del día y su % de variación."""
    return repo.buscar(producto, categoria)
