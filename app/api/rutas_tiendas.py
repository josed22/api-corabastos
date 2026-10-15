from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.tienda import Tienda
from app.repositories.tienda_repo import TiendaRepository

router = APIRouter(prefix="/tiendas", tags=["Tiendas"])
repo = TiendaRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_tiendas(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{tienda_id}")
def obtener_tienda(tienda_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(tienda_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return registro


@router.post("/", status_code=201)
def crear_tienda(tienda: Tienda, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = tienda.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Tienda registrada exitosamente", "id": nuevo_id}


@router.put("/{tienda_id}")
def actualizar_tienda(tienda_id: int, tienda: Tienda, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = tienda.model_dump()
    exito = repo.actualizar(tienda_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return {"mensaje": "Tienda actualizada correctamente"}


@router.delete("/{tienda_id}")
def eliminar_tienda(tienda_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(tienda_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return {"mensaje": "Tienda eliminada correctamente"}
