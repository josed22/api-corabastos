from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.reserva import Reserva
from app.repositories.reserva_repo import ReservaRepository

router = APIRouter(prefix="/reservas", tags=["Reservas"])
repo = ReservaRepository()
ROLES_ESCRITURA = ("Administrador", "Vendedor", "Comprador")


@router.get("/")
def listar_reservas(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{reserva_id}")
def obtener_reserva(reserva_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(reserva_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return registro


@router.post("/", status_code=201)
def crear_reserva(reserva: Reserva, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = reserva.model_dump()
    if actual["rol"] == "Comprador" or not datos.get("id_usuario"):
        datos["id_usuario"] = actual["id"]  # el comprador solo reserva a su nombre
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Reserva registrada exitosamente", "id": nuevo_id}


@router.put("/{reserva_id}")
def actualizar_reserva(reserva_id: int, reserva: Reserva, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = reserva.model_dump()
    if actual["rol"] == "Comprador" or not datos.get("id_usuario"):
        datos["id_usuario"] = actual["id"]  # el comprador solo reserva a su nombre
    exito = repo.actualizar(reserva_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"mensaje": "Reserva actualizada correctamente"}


@router.delete("/{reserva_id}")
def eliminar_reserva(reserva_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(reserva_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"mensaje": "Reserva eliminada correctamente"}
