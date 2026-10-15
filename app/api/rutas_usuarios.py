from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencias import obtener_usuario_actual, requiere_roles
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
repo = UsuarioRepository()
ROLES_ESCRITURA = ("Administrador",)


@router.get("/")
def listar_usuarios(incluir_inactivos: bool = False, actual: dict = Depends(requiere_roles("Administrador"))):
    return repo.obtener_todos(incluir_inactivos)


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int, actual: dict = Depends(requiere_roles("Administrador"))):
    registro = repo.obtener_por_id(usuario_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return registro


@router.post("/", status_code=201)
def crear_usuario(usuario: Usuario, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = usuario.model_dump()
    nuevo_id = repo.crear(datos)
    return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}


@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: Usuario, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    datos = usuario.model_dump()
    exito = repo.actualizar(usuario_id, datos)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario actualizado correctamente"}


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, actual: dict = Depends(requiere_roles(*ROLES_ESCRITURA))):
    """Eliminado lógico: el registro no se borra, su estado pasa a falso."""
    exito = repo.eliminar(usuario_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}
