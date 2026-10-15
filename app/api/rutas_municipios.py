from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.municipio import Municipio
from app.repositories.municipio_repo import MunicipioRepository

router = APIRouter(prefix="/municipios", tags=["Municipios"])
repo = MunicipioRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_municipios(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{municipio_id}")
def obtener_municipio(municipio_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(municipio_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_municipio(municipio: Municipio, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = municipio.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Municipio registrado exitosamente", "id": nuevo_id}


@router.put("/{municipio_id}")
def actualizar_municipio(municipio_id: int, municipio: Municipio, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = municipio.model_dump()
    exito = repo.actualizar(municipio_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return {"mensaje": "Municipio actualizado correctamente"}


@router.delete("/{municipio_id}")
def eliminar_municipio(municipio_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(municipio_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return {"mensaje": "Municipio eliminado correctamente"}
