from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.modulo import Modulo
from app.repositories.modulo_repo import ModuloRepository

router = APIRouter(prefix="/modulos", tags=["Módulos"])
repo = ModuloRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_modulos(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{modulo_id}")
def obtener_modulo(modulo_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(modulo_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_modulo(modulo: Modulo, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = modulo.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Módulo registrado exitosamente", "id": nuevo_id}


@router.put("/{modulo_id}")
def actualizar_modulo(modulo_id: int, modulo: Modulo, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = modulo.model_dump()
    exito = repo.actualizar(modulo_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return {"mensaje": "Módulo actualizado correctamente"}


@router.delete("/{modulo_id}")
def eliminar_modulo(modulo_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(modulo_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return {"mensaje": "Módulo eliminado correctamente"}
