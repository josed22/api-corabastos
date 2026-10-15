# API Corabastos (FastAPI + PostgreSQL)

API para consultar los precios del día de Corabastos, ver qué bodega tiene cada producto y reservarlo.
Estructura por capas: `app/api` (rutas) → `app/repositories` (SQL) → `app/models` (Pydantic) → `app/core` (conexión, JWT, errores).

## Ejecutar en local

```bash
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # y completar los datos de la base
uvicorn main:app --reload   # http://127.0.0.1:8000/docs
```

La base se crea con `db/corabastos.sql` (16 tablas, 2 vistas y datos de ejemplo). Ejecutarlo completo en una base vacía.

## Autenticación (JWT)

1. `POST /auth/login` con `{"correo": "...", "password": "..."}` devuelve `access_token`, el usuario y sus módulos.
2. Enviar `Authorization: Bearer <token>` en las demás peticiones (en `/docs`, botón **Authorize**).
3. El token se valida en cada petición (firma, expiración, usuario activo). Sin token o con token inválido: `401`; rol sin permiso: `403`.

Usuarios de ejemplo (contraseña `Clave2025*`): `laura.gomez@gmail.com` (Administrador), `carlos.rodriguez@gmail.com` (Vendedor), `andres.martinez@gmail.com` (Comprador).

## Reglas

- Todas las tablas tienen `estado`, `creado` y `actualizado`. `DELETE` es lógico: pone `estado = false`, no borra el registro.
- Solo el **Administrador** crea, edita y elimina datos maestros y fija los **precios del día**.
- El **Vendedor** administra el inventario de su bodega (solo productos de la categoría de su pabellón) y atiende reservas.
- El **Comprador** consulta el catálogo y crea reservas a su nombre. El precio unitario sale del precio del día.
- Variación porcentual de precios: `GET /precios-dia/variacion` y `GET /catalogo/`.

## Despliegue (Render)

Ver `render.yaml`. Resumen: base PostgreSQL en la nube → subir este proyecto a GitHub → crear un *Web Service* en Render →
cargar las variables `DB_*` → comando de inicio `uvicorn main:app --host 0.0.0.0 --port $PORT`.
