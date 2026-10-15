from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.estado_reserva import EstadoReserva
from app.repositories.estado_reserva_repo import EstadoReservaRepository

router = APIRouter(prefix="/estados-reserva", tags=["Estados de reserva"])
repo = EstadoReservaRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_estados_reserva(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{estado_reserva_id}")
def obtener_estado_reserva(estado_reserva_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(estado_reserva_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Estado de reserva no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_estado_reserva(estado_reserva: EstadoReserva, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = estado_reserva.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Estado de reserva registrado exitosamente", "id": nuevo_id}


@router.put("/{estado_reserva_id}")
def actualizar_estado_reserva(estado_reserva_id: int, estado_reserva: EstadoReserva, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = estado_reserva.model_dump()
    exito = repo.actualizar(estado_reserva_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Estado de reserva no encontrado")
    return {"mensaje": "Estado de reserva actualizado correctamente"}


@router.delete("/{estado_reserva_id}")
def eliminar_estado_reserva(estado_reserva_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(estado_reserva_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Estado de reserva no encontrado")
    return {"mensaje": "Estado de reserva eliminado correctamente"}
