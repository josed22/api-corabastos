from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.categoria import Categoria
from app.repositories.categoria_repo import CategoriaRepository

router = APIRouter(prefix="/categorias", tags=["Categorías"])
repo = CategoriaRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_categorias(incluir_inactivos: bool = False, actual: dict = Depends(obtener_usuario_actual)):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int, actual: dict = Depends(obtener_usuario_actual)):
    registro = repo.obtener_por_id(categoria_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return registro


@router.post("/", status_code=201)
def crear_categoria(categoria: Categoria, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = categoria.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Categoría registrada exitosamente", "id": nuevo_id}


@router.put("/{categoria_id}")
def actualizar_categoria(categoria_id: int, categoria: Categoria, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = categoria.model_dump()
    exito = repo.actualizar(categoria_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"mensaje": "Categoría actualizada correctamente"}


@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(categoria_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"mensaje": "Categoría eliminada correctamente"}
