from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.tipo import Tipo
from app.repositories.tipo_repo import TipoRepository

router = APIRouter(prefix="/tipos", tags=["Tipos"])
repo = TipoRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_tipos(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{tipo_id}")
def obtener_tipo(tipo_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(tipo_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_tipo(tipo: Tipo, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = tipo.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Tipo registrado exitosamente", "id": nuevo_id}


@router.put("/{tipo_id}")
def actualizar_tipo(tipo_id: int, tipo: Tipo, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = tipo.model_dump()
    exito = repo.actualizar(tipo_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return {"mensaje": "Tipo actualizado correctamente"}


@router.delete("/{tipo_id}")
def eliminar_tipo(tipo_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(tipo_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return {"mensaje": "Tipo eliminado correctamente"}
