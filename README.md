# Práctica 2 PWII — Backend en Python con arquitectura limpia e IA

Reescritura del backend de la [Práctica 1](https://github.com/ikercelaya/Practica1PWII)
(originalmente **Node.js + Express + MongoDB + Redis**) por un backend nuevo desarrollado
**íntegramente en Python con FastAPI**, manteniendo el **mismo contrato de API** (mismas URLs,
métodos y formato JSON) para que el frontend **Svelte 5** siga funcionando con su misma lógica de
consumo de API. Como **mejora añadida** sobre la Práctica 1 se incorpora la **edición de la imagen
del producto** (ver §6).

El foco de la entrega es la **separación de responsabilidades en capas**, la **autenticación
JWT**, la **validación estricta**, el **manejo global de errores**, la **persistencia real con
ORM** y el **uso documentado y crítico de la IA** (ver [`MEMORIA_IA.md`](MEMORIA_IA.md)).

---

## 1. Tecnologías

| Capa | Tecnología |
|------|-----------|
| Framework web | **FastAPI** |
| Servidor ASGI | Uvicorn |
| Validación / serialización | **Pydantic v2** |
| ORM / persistencia | **SQLAlchemy 2.0** sobre **SQLite** |
| Autenticación | **JWT** (PyJWT) + **bcrypt** |
| Frontend | Svelte 5 + Vite (reutilizado de la Práctica 1) |

> Se eligió **FastAPI** frente a Flask porque sus dependencias nativas (Pydantic para
> validación con `422`, inyección de dependencias para proteger rutas, manejadores de
> excepciones y documentación OpenAPI automática) encajan directamente con los criterios
> de la rúbrica.

---

## 2. Arquitectura (separación de responsabilidades)

El código está organizado en capas con una única responsabilidad cada una. **El archivo de
arranque (`app/main.py`) no contiene lógica de negocio**: sólo ensambla la aplicación.

```
backend/
├── app/
│   ├── main.py                 # Fábrica de la app: CORS, estáticos, routers, handlers
│   ├── core/                   # Núcleo transversal
│   │   ├── config.py           #   Configuración (pydantic-settings)
│   │   ├── database.py         #   Motor, sesión y Base de SQLAlchemy
│   │   ├── security.py         #   Hashing bcrypt + emisión/validación de JWT
│   │   ├── exceptions.py       #   Excepciones de dominio (sin acoplar a HTTP)
│   │   └── error_handlers.py   #   Manejo GLOBAL de excepciones -> JSON unificado
│   ├── models/                 # Modelos ORM (SQLAlchemy)         [acceso a datos]
│   │   ├── user.py · producto.py · cart.py
│   ├── schemas/                # Esquemas Pydantic (validación + salida)
│   │   ├── auth.py · producto.py · user.py · cart.py
│   ├── repositories/           # Patrón Repositorio: ÚNICO acceso a la BD
│   │   ├── user_repository.py · producto_repository.py · cart_repository.py
│   ├── services/               # Lógica de negocio (no sabe de HTTP ni de SQL)
│   │   ├── auth_service.py · producto_service.py · user_service.py · cart_service.py
│   ├── dependencies/           # Guards de FastAPI (JWT, require_admin)
│   │   └── auth.py
│   ├── routers/                # Controladores HTTP: validan, delegan y responden
│   │   ├── auth_router.py · producto_router.py · user_router.py · cart_router.py
│   └── utils/                  # Utilidades (guardado de imágenes)
│       └── files.py
├── seed.py                     # Datos iniciales (usuarios + productos de ejemplo)
├── run.py                      # Arranque cómodo del servidor
├── requirements.txt
└── .env.example
```

**Flujo de una petición:** `router` (HTTP) → `service` (negocio) → `repository` (SQL) → `model` (ORM).
La validación de entrada la hacen los **schemas** y la autorización las **dependencies**.

---

## 3. Instalación y ejecución

### Requisitos previos
- **Python 3.11+** (probado con 3.13)
- **Node.js 18+** (para el frontend)

> No hace falta MongoDB ni Redis (a diferencia de la Práctica 1): la persistencia es
> **SQLite**, que se crea sola en un archivo.

Se necesitan **dos terminales**: una para el backend y otra para el frontend.

### 3.1. Backend (Terminal 1) — PowerShell (Windows)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env      # crea la configuración local
python seed.py                   # crea usuarios y productos de ejemplo
python run.py                    # arranca en http://localhost:3000
```

En Linux/macOS:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
python run.py
```

Alternativa de arranque equivalente a `run.py`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
```

Cuando arranca correctamente, la API está en `http://localhost:3000/api` y la
**documentación interactiva (Swagger/OpenAPI)** en `http://localhost:3000/docs`.

### 3.2. Frontend (Terminal 2)

```powershell
cd frontend
Copy-Item .env.example .env      # apunta a http://localhost:3000/api
npm install
npm run dev                      # arranca en http://localhost:5173
```

Abre `http://localhost:5173` e inicia sesión con los usuarios de prueba.

### 3.3. Usuarios de prueba (creados por `seed.py`)

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `admin123` | admin |
| `user`  | `user123`  | user |

---

## 4. Endpoints utilizados y roles necesarios

Base: `http://localhost:3000/api` · Imágenes: `http://localhost:3000/uploads/<archivo>`

| Método | Ruta | ¿Auth? | Rol | Descripción |
|--------|------|--------|-----|-------------|
| POST | `/api/login` | No | — | Devuelve `{ "token": "<jwt>" }` |
| POST | `/api/register` | No | — | Alta de usuario (siempre rol `user`) |
| GET | `/api/productos` | No | — | Listado (acepta `?name=` para filtrar) |
| POST | `/api/productos` | Sí | **admin** | Crear producto (`multipart/form-data` con imagen) |
| PUT | `/api/productos/{id}` | Sí | **admin** | Editar producto (`multipart/form-data`; imagen opcional para reemplazarla) |
| DELETE | `/api/productos/{id}` | Sí | **admin** | Borrar producto |
| GET | `/api/users` | Sí | **admin** | Listar usuarios (sin contraseña) |
| POST | `/api/users` | Sí | **admin** | Crear usuario |
| PUT | `/api/users/{id}` | Sí | **admin** | Editar usuario |
| DELETE | `/api/users/{id}` | Sí | **admin** | Borrar usuario |
| GET | `/api/cart` | Sí | user/admin | Ver carrito del usuario autenticado |
| POST | `/api/cart/add` | Sí | user/admin | Añadir producto (`{ "productId": <id> }`) |
| DELETE | `/api/cart/{productId}` | Sí | user/admin | Quitar producto del carrito |

**Roles:**
- `user`: inicia sesión, ve productos y gestiona su carrito.
- `admin`: además crea/edita/borra productos y gestiona usuarios.

**Semántica de errores de autenticación** (idéntica al backend original):
- Sin cabecera `Authorization` → **401**
- Token inválido o expirado → **403**
- Autenticado pero sin rol `admin` en ruta de admin → **403** (`{"error": "Solo admin"}`)

---

## 5. Compatibilidad del contrato con el frontend

El backend reproduce el contrato que ya esperaba el frontend Svelte 5 de la Práctica 1, que
conserva su lógica de consumo de API:

- El login devuelve `{ token }` y el JWT lleva el payload `{ id, username, role }`, que el
  frontend decodifica para conocer el rol.
- Todos los recursos exponen su identificador como **`_id`** (igual que MongoDB), incluido
  el producto "populado" dentro de cada línea del carrito (`item.productId._id`).
- `GET /api/productos` y `GET /api/users` devuelven **arrays** directamente.
- Las imágenes se sirven en `/uploads/<archivo>` y el producto guarda sólo el nombre del
  archivo en el campo `imagen`.
- Los errores se devuelven con la clave `error`, que es justo lo que lee el cliente
  (`data.error || data.message`) para mostrar el toast.

---

## 6. Funcionalidades avanzadas implementadas

- **Validación estricta (Pydantic):** todos los cuerpos de entrada se validan con esquemas
  (`schemas/`). Datos inválidos → **`422 Unprocessable Entity`** con mensaje estructurado.
- **Manejo global de excepciones:** `core/error_handlers.py` captura excepciones de dominio,
  de validación e inesperadas y las traduce a un JSON unificado `{error, status_code, detail}`.
- **Persistencia real + patrón repositorio:** SQLite mediante SQLAlchemy. Todo el acceso a
  datos está encapsulado en `repositories/`; ni servicios ni routers ejecutan SQL. **No se usa
  ninguna persistencia simulada** (ni listas en memoria, ni JSON, ni archivos de texto).
- **Edición de la imagen del producto (mejora sobre la P1):** el formulario de edición permite
  subir una imagen nueva. `PUT /api/productos/{id}` acepta `multipart/form-data` y reemplaza la
  imagen **sólo si se adjunta** una; si no, conserva la actual (actualización parcial). Implicó un
  cambio mínimo en el frontend (`ProductForm.svelte`, `AdminPage.svelte`, `lib/api.js`).

---

## 7. Correspondencia con la rúbrica

| Criterio | Dónde se cumple |
|----------|-----------------|
| Estructura y separación en capas | `routers/` → `services/` → `repositories/` → `models/`; `main.py` sin lógica |
| Autenticación JWT compatible | `core/security.py`, `dependencies/auth.py`, `routers/auth_router.py` |
| Migración del contrato (mismas URLs y métodos) | Sección 5 y pruebas de humo (30/30) |
| IA: registro de prompts | [`MEMORIA_IA.md`](MEMORIA_IA.md) §2 |
| IA: análisis crítico de errores | [`MEMORIA_IA.md`](MEMORIA_IA.md) §3 |
| Validaciones y errores (Pydantic + 422 + handler global) | `schemas/`, `core/error_handlers.py` |
| Base de datos (ORM) + repositorio | `core/database.py`, `models/`, `repositories/` |

---

## 8. Verificación realizada

- **Importación y rutas:** la app levanta y registra las 13 rutas del contrato.
- **Pruebas de contrato end-to-end:** batería de 30 comprobaciones (auth, productos,
  usuarios, carrito, validaciones 422, roles 401/403, filtro por nombre, `_id` anidado) →
  **30/30 correctas**.
- **Edición de imagen:** batería específica de **11/11** comprobaciones (subir y reemplazar
  imagen, conservar la actual si no se envía, actualización parcial, validación 422 y rol admin).
- **Frontend:** compila con `npm run build` (también verificado en navegador real cross-origin).

---

## 9. Entrega

- Código en repositorio público (este repo).
- Memoria del uso de IA en [`MEMORIA_IA.md`](MEMORIA_IA.md).
- Endpoints principales y roles documentados en la sección 4.
