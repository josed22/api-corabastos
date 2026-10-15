from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from typing import Optional
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.precio_dia import PrecioDia
from app.repositories.precio_dia_repo import PrecioDiaRepository

router = APIRouter(prefix="/precios-dia", tags=["Precios del día"])
repo = PrecioDiaRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/variacion")
def variacion_de_precios(fecha: Optional[date] = None, actual: dict = Depends(obtener_usuario_actual)):
    """Precio de cada producto en la fecha indicada (hoy por defecto) y su % de subida o bajada."""
    return repo.variaciones(fecha)


@router.get("/variacion/{producto_id}")
def historial_de_variacion(producto_id: int, actual: dict = Depends(obtener_usuario_actual)):
    """Historial diario de precios de un producto con su % de variación."""
    return repo.historial_variacion(producto_id)



@router.get("/")
def listar_precios_dia(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{precio_dia_id}")
def obtener_precio_dia(precio_dia_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(precio_dia_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Precio del día no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_precio_dia(precio_dia: PrecioDia, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = precio_dia.model_dump()
    datos["id_usuario"] = actual["id"]  # el administrador que fija el precio sale del token
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Precio del día registrado exitosamente", "id": nuevo_id}


@router.put("/{precio_dia_id}")
def actualizar_precio_dia(precio_dia_id: int, precio_dia: PrecioDia, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = precio_dia.model_dump()
    datos["id_usuario"] = actual["id"]  # el administrador que fija el precio sale del token
    exito = repo.actualizar(precio_dia_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Precio del día no encontrado")
    return {"mensaje": "Precio del día actualizado correctamente"}


@router.delete("/{precio_dia_id}")
def eliminar_precio_dia(precio_dia_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(precio_dia_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Precio del día no encontrado")
    return {"mensaje": "Precio del día eliminado correctamente"}
