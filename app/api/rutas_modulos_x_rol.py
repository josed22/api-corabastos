from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.modulo_x_rol import ModuloXRol
from app.repositories.modulo_x_rol_repo import ModuloXRolRepository

router = APIRouter(prefix="/modulos-por-rol", tags=["Módulos por rol"])
repo = ModuloXRolRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_modulos_x_rol(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{modulo_x_rol_id}")
def obtener_modulo_x_rol(modulo_x_rol_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(modulo_x_rol_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Asignación de módulo a rol no encontrada")
    return registro


@router.post("/", status_code=201)
def crear_modulo_x_rol(modulo_x_rol: ModuloXRol, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = modulo_x_rol.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Asignación de módulo a rol registrada exitosamente", "id": nuevo_id}


@router.put("/{modulo_x_rol_id}")
def actualizar_modulo_x_rol(modulo_x_rol_id: int, modulo_x_rol: ModuloXRol, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = modulo_x_rol.model_dump()
    exito = repo.actualizar(modulo_x_rol_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Asignación de módulo a rol no encontrada")
    return {"mensaje": "Asignación de módulo a rol actualizada correctamente"}


@router.delete("/{modulo_x_rol_id}")
def eliminar_modulo_x_rol(modulo_x_rol_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(modulo_x_rol_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Asignación de módulo a rol no encontrada")
    return {"mensaje": "Asignación de módulo a rol eliminada correctamente"}
