from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.detalle_reserva import DetalleReserva
from app.repositories.detalle_reserva_repo import DetalleReservaRepository

router = APIRouter(prefix="/detalle-reservas", tags=["Detalle de reservas"])
repo = DetalleReservaRepository()
ROLES_ESCRITURA = ("Administrador", "Vendedor", "Comprador")


@router.get("/")
def listar_detalles_reserva(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{detalle_reserva_id}")
def obtener_detalle_reserva(detalle_reserva_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(detalle_reserva_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_detalle_reserva(detalle_reserva: DetalleReserva, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = detalle_reserva.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Detalle de reserva registrado exitosamente", "id": nuevo_id}


@router.put("/{detalle_reserva_id}")
def actualizar_detalle_reserva(detalle_reserva_id: int, detalle_reserva: DetalleReserva, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = detalle_reserva.model_dump()
    exito = repo.actualizar(detalle_reserva_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    return {"mensaje": "Detalle de reserva actualizado correctamente"}


@router.delete("/{detalle_reserva_id}")
def eliminar_detalle_reserva(detalle_reserva_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(detalle_reserva_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    return {"mensaje": "Detalle de reserva eliminado correctamente"}
