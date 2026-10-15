from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import TokenError, decodificar_token
from app.repositories.usuario_repo import UsuarioRepository

esquema_bearer = HTTPBearer(auto_error=False)
usuario_repo = UsuarioRepository()


def _no_autenticado(detalle: str):
    return HTTPException(status_code=401, detail=detalle, headers={"WWW-Authenticate": "Bearer"})


def obtener_usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(esquema_bearer)) -> dict:
    """Valida el token JWT y devuelve el usuario activo (con su rol) al que pertenece."""
    if credenciales is None:
        raise _no_autenticado("Falta el token de autenticación")
    try:
        payload = decodificar_token(credenciales.credentials)
        usuario_id = int(payload["sub"])
    except TokenError as e:
        raise _no_autenticado(str(e))
    except (KeyError, ValueError):
        raise _no_autenticado("Token inválido")

    usuario = usuario_repo.obtener_activo_con_rol(usuario_id)
    if not usuario:
        raise _no_autenticado("El usuario no existe o está inactivo")
    return usuario


def requiere_roles(*roles: str):
    """Dependencia que solo deja pasar a los usuarios con alguno de los roles indicados."""
    def verificador(actual: dict = Depends(obtener_usuario_actual)) -> dict:
        if actual["rol"] not in roles:
            raise HTTPException(status_code=403, detail=f"Acceso denegado: se requiere el rol {' o '.join(roles)}")
        return actual
    return verificador
