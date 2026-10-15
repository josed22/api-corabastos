from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.inventario import Inventario
from app.repositories.inventario_repo import InventarioRepository

router = APIRouter(prefix="/inventario", tags=["Inventario"])
repo = InventarioRepository()
ROLES_ESCRITURA = ("Administrador", "Vendedor")


@router.get("/")
def listar_inventarios(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{inventario_id}")
def obtener_inventario(inventario_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(inventario_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_inventario(inventario: Inventario, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = inventario.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Inventario registrado exitosamente", "id": nuevo_id}


@router.put("/{inventario_id}")
def actualizar_inventario(inventario_id: int, inventario: Inventario, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = inventario.model_dump()
    exito = repo.actualizar(inventario_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return {"mensaje": "Inventario actualizado correctamente"}


@router.delete("/{inventario_id}")
def eliminar_inventario(inventario_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(inventario_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return {"mensaje": "Inventario eliminado correctamente"}
