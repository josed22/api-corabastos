from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.rol import Rol
from app.repositories.rol_repo import RolRepository

router = APIRouter(prefix="/roles", tags=["Roles"])
repo = RolRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_roles(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{rol_id}")
def obtener_rol(rol_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(rol_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_rol(rol: Rol, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = rol.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Rol registrado exitosamente", "id": nuevo_id}


@router.put("/{rol_id}")
def actualizar_rol(rol_id: int, rol: Rol, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = rol.model_dump()
    exito = repo.actualizar(rol_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"mensaje": "Rol actualizado correctamente"}


@router.delete("/{rol_id}")
def eliminar_rol(rol_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(rol_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"mensaje": "Rol eliminado correctamente"}
