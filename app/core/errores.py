import psycopg2
from psycopg2 import errors
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ReglaDeNegocioError(Exception):
    """Se lanza cuando una petición válida incumple una regla del negocio."""


def _respuesta(codigo: int, detalle: str):
    return JSONResponse(status_code=codigo, content={"detail": detalle})


def registrar_manejadores(app: FastAPI):
    @app.exception_handler(ReglaDeNegocioError)
    async def regla_de_negocio(request: Request, exc: ReglaDeNegocioError):
        return _respuesta(400, str(exc))

    @app.exception_handler(errors.UniqueViolation)
    async def valor_duplicado(request: Request, exc: errors.UniqueViolation):
        return _respuesta(409, f"Ya existe un registro con ese valor único. {exc.diag.message_detail or ''}".strip())

    @app.exception_handler(errors.ForeignKeyViolation)
    async def llave_foranea(request: Request, exc: errors.ForeignKeyViolation):
        return _respuesta(400, f"Referencia a un registro que no existe. {exc.diag.message_detail or ''}".strip())

    @app.exception_handler(errors.CheckViolation)
    async def restriccion(request: Request, exc: errors.CheckViolation):
        return _respuesta(400, "El valor enviado incumple una restricción de la tabla")

    @app.exception_handler(errors.NotNullViolation)
    async def campo_obligatorio(request: Request, exc: errors.NotNullViolation):
        return _respuesta(400, "Falta un campo obligatorio")

    @app.exception_handler(psycopg2.OperationalError)
    async def bd_no_disponible(request: Request, exc: psycopg2.OperationalError):
        return _respuesta(503, "La base de datos no está disponible")

    @app.exception_handler(ConnectionError)
    async def sin_conexion(request: Request, exc: ConnectionError):
        return _respuesta(503, str(exc))
