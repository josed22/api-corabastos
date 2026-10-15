from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.producto import Producto
from app.repositories.producto_repo import ProductoRepository

router = APIRouter(prefix="/productos", tags=["Productos"])
repo = ProductoRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_productos(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{producto_id}")
def obtener_producto(producto_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(producto_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_producto(producto: Producto, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = producto.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Producto registrado exitosamente", "id": nuevo_id}


@router.put("/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = producto.model_dump()
    exito = repo.actualizar(producto_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto actualizado correctamente"}


@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(producto_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado correctamente"}
