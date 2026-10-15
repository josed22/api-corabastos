from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.pabellon import Pabellon
from app.repositories.pabellon_repo import PabellonRepository

router = APIRouter(prefix="/pabellones", tags=["Pabellones"])
repo = PabellonRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_pabellones(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{pabellon_id}")
def obtener_pabellon(pabellon_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(pabellon_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Pabellón no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_pabellon(pabellon: Pabellon, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = pabellon.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Pabellón registrado exitosamente", "id": nuevo_id}


@router.put("/{pabellon_id}")
def actualizar_pabellon(pabellon_id: int, pabellon: Pabellon, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = pabellon.model_dump()
    exito = repo.actualizar(pabellon_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Pabellón no encontrado")
    return {"mensaje": "Pabellón actualizado correctamente"}


@router.delete("/{pabellon_id}")
def eliminar_pabellon(pabellon_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(pabellon_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Pabellón no encontrado")
    return {"mensaje": "Pabellón eliminado correctamente"}
