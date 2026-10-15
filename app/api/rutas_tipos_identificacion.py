from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.tipo_identificacion import TipoIdentificacion
from app.repositories.tipo_identificacion_repo import TipoIdentificacionRepository

router = APIRouter(prefix="/tipos-identificacion", tags=["Tipos de identificación"])
repo = TipoIdentificacionRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_tipos_identificacion(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{tipo_identificacion_id}")
def obtener_tipo_identificacion(tipo_identificacion_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(tipo_identificacion_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Tipo de identificación no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_tipo_identificacion(tipo_identificacion: TipoIdentificacion, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = tipo_identificacion.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Tipo de identificación registrado exitosamente", "id": nuevo_id}


@router.put("/{tipo_identificacion_id}")
def actualizar_tipo_identificacion(tipo_identificacion_id: int, tipo_identificacion: TipoIdentificacion, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = tipo_identificacion.model_dump()
    exito = repo.actualizar(tipo_identificacion_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Tipo de identificación no encontrado")
    return {"mensaje": "Tipo de identificación actualizado correctamente"}


@router.delete("/{tipo_identificacion_id}")
def eliminar_tipo_identificacion(tipo_identificacion_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(tipo_identificacion_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Tipo de identificación no encontrado")
    return {"mensaje": "Tipo de identificación eliminado correctamente"}
