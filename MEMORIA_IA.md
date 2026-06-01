# Memoria del uso de Inteligencia Artificial — Práctica 2 PWII

> Documento que registra cómo se ha utilizado la IA como **asistente de desarrollo** (no como
> generador ciego de código) para construir el backend en Python, qué **prompts clave** se
> emplearon, cómo se **refinaron** cuando el primer resultado no fue satisfactorio y qué
> **errores/alucinaciones** cometió la IA, con su correspondiente **corrección manual**.

## 1. Herramientas y metodología

- **Herramientas usadas:** asistente conversacional (ChatGPT / Claude) para diseño y
  refactorización, y autocompletado tipo Copilot para código repetitivo.
- **Metodología:** la IA se usó para **acelerar** tareas concretas (configurar JWT, esquema de
  capas, esquemas Pydantic), pero **todo el código generado se revisó, se probó y se corrigió
  manualmente** aplicando los conceptos vistos en clase (separación de responsabilidades,
  seguridad, semántica REST, patrón repositorio). El criterio para aceptar una respuesta fue
  siempre: *“¿mantiene el contrato del frontend y respeta las capas?”*.

---

## 2. Registro de prompts clave e iteraciones

### Prompt 1 — Estructura del proyecto en capas

**Prompt inicial:**
> «Crea un backend en FastAPI para un CRUD de productos y usuarios con login JWT.»

**Resultado:** la IA generó **un único archivo `main.py`** con todas las rutas, el acceso a la
base de datos y la firma del JWT mezclados. Funcionaba, pero **incumplía el requisito principal
de la práctica** (separación de responsabilidades; prohibido centralizar todo en el archivo de
enrutado).

**Refinamiento del prompt:**
> «Reescríbelo separando en capas: `routers` (sólo HTTP), `services` (lógica de negocio),
> `repositories` (único acceso a datos con SQLAlchemy), `models` (ORM) y `schemas` (Pydantic).
> El `main.py` sólo debe ensamblar la app. Inyecta la sesión de BD con `Depends`.»

**Resultado final:** la estructura por capas que hay en `app/`. A partir de aquí, cada prompt
posterior se acotó **a una sola capa** para que la IA no volviera a mezclar responsabilidades.

### Prompt 2 — Compatibilidad del identificador `_id`

**Prompt inicial:**
> «Devuelve los productos con FastAPI desde SQLAlchemy.»

**Resultado:** la IA devolvía el campo como `id` (entero). El frontend de la Práctica 1 espera
`_id` (herencia de MongoDB) y se rompía: `product._id` era `undefined` y fallaban tanto las
`key` de los `{#each}` como el carrito (`item.productId._id`).

**Refinamiento del prompt:**
> «El JSON de salida debe usar `_id` en vez de `id` para no tocar el frontend, pero leyendo el
> atributo `id` del modelo ORM. Hazlo con Pydantic v2.»

**Resultado final:** en `schemas/producto.py` y `schemas/user.py` se usa
`id: int = Field(serialization_alias="_id")` junto con `from_attributes=True`, y FastAPI
serializa con `by_alias`. (El primer intento de la IA con `alias="_id"` rompía la lectura desde
el ORM; ver §3, caso 2.)

### Prompt 3 — Configuración del JWT y protección de rutas

**Prompt inicial:**
> «Protege las rutas con JWT en FastAPI.»

**Resultado:** la IA propuso `HTTPBearer` de FastAPI. El problema: `HTTPBearer(auto_error=True)`
devuelve **403** cuando **falta** el token, pero el contrato original distingue **401 (sin
cabecera)** de **403 (token inválido/expirado)**.

**Refinamiento del prompt:**
> «Necesito reproducir el middleware original: si no hay cabecera `Authorization` → 401; si el
> token es inválido o ha expirado → 403; y un guard `require_admin` que devuelva 403 con
> `{"error": "Solo admin"}`.»

**Resultado final:** dependencia propia `get_current_user` / `require_admin` en
`dependencies/auth.py`, que reproduce exactamente esa semántica.

### Prompt 4 — Validación estricta y manejo global de errores

**Prompt:**
> «Quiero validar los datos con Pydantic y un manejador global de excepciones que devuelva
> siempre el mismo formato JSON de error, incluyendo el `422` de validación. El cuerpo de error
> debe tener una clave `error` porque el frontend lee `data.error`.»

**Resultado final:** esquemas en `schemas/` + `core/error_handlers.py` con manejadores para
`RequestValidationError`, `ValidationError` de Pydantic, excepciones de dominio (`AppError`),
`HTTPException` y un *catch-all* para errores inesperados (500).

### Prompt 5 — Subida de imágenes (multipart)

**Prompt:**
> «El endpoint de crear producto recibe `multipart/form-data` con `nombre`, `precio` e `imagen`
> (archivo opcional). Guarda la imagen en `uploads/` con nombre único y guarda sólo el nombre en
> la BD; sírvela en `/uploads`.»

**Resultado final:** `utils/files.py` (nombre con `uuid4`) + `StaticFiles` montado en `/uploads`
en `main.py`, replicando el comportamiento de `multer` del backend original.

---

## 3. Análisis crítico: errores y alucinaciones de la IA

### Caso 1 — Fuga de seguridad: la IA devolvía el hash de la contraseña

**Qué generó la IA.** Al pedirle el endpoint `GET /api/users`, devolvió directamente los objetos
del modelo, de modo que la respuesta incluía el campo `password` (el hash bcrypt):

```python
@router.get("/users")
def get_users(db = Depends(get_db)):
    return db.query(User).all()   # ⚠️ expone el hash de la contraseña
```

**Por qué es incorrecto.** Es un **fallo de seguridad**: exponer hashes facilita ataques de
fuerza bruta/diccionario offline y filtra información sensible. Además **acopla** el modelo de
persistencia a la respuesta HTTP (cualquier columna nueva se filtraría sola).

**Corrección manual (conceptos de clase: DTO/esquemas de salida y mínimo privilegio).** Se
introdujo un esquema de salida `UserOut` que **sólo** expone `_id`, `username` y `role`, y el
repositorio nunca devuelve el hash al exterior. El backend original ya hacía esto con
`User.find({}, '-password')`; aquí se replica con un esquema Pydantic explícito.

### Caso 2 — Alucinación sobre los alias de Pydantic v2 (`alias` vs `serialization_alias`)

**Qué generó la IA.** Para que la salida usara `_id`, propuso:

```python
class ProductoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int = Field(alias="_id")
```

y aseguraba que “así se lee `id` del ORM y se devuelve `_id`”.

**Por qué es incorrecto/subóptimo.** En Pydantic v2, `alias` afecta **a la vez** a la
**validación** y a la **serialización**. Con `from_attributes=True`, Pydantic intentaba leer el
atributo **`_id`** del objeto ORM (que **no existe**, el atributo se llama `id`), lo que provoca
error de validación o un valor vacío. Es una **alucinación clásica**: mezcla el comportamiento de
Pydantic v1 (`allow_population_by_field_name`) con v2 y no distingue alias de validación de alias
de serialización.

**Corrección manual.** Tras leer la documentación de Pydantic v2, se separó el alias **sólo de
salida**:

```python
id: int = Field(serialization_alias="_id")   # lee .id del ORM, escribe "_id" en el JSON
```

`serialization_alias` afecta únicamente al volcado, y FastAPI serializa con `by_alias=True`,
así que el ORM se lee por `id` y el cliente recibe `_id`. Verificado en las pruebas: el carrito
anidado también emite `productId._id` correctamente.

### Caso 3 — Persistencia simulada y `bcrypt` mal integrado

**Qué generó la IA (dos sub-errores).**
1. Para “ir rápido”, propuso guardar los datos en **listas/diccionarios en memoria** y, como
   alternativa, `create_engine("sqlite:///:memory:")`.
2. Para el hashing, sugirió `passlib` con `CryptContext(schemes=["bcrypt"])`.

**Por qué es incorrecto.**
1. La rúbrica **prohíbe explícitamente** la persistencia simulada (memoria, JSON, texto plano).
   Además, `sqlite:///:memory:` **pierde los datos** entre conexiones/peticiones, así que ni
   siquiera sirve como base de datos real.
2. `passlib` 1.7.x es **incompatible** con `bcrypt` ≥ 4: lanza el aviso
   `(trapped) error reading bcrypt version` / `AttributeError: module 'bcrypt' has no attribute
   '__about__'`. Es una dependencia frágil y ruidosa para algo que `bcrypt` ya resuelve solo.

**Corrección manual (conceptos de clase: capa de persistencia y patrón repositorio).**
1. Se usa **SQLite en archivo** (`sqlite:///./practica2.db`) con **SQLAlchemy**, y **todo** el
   acceso a datos queda encapsulado en `repositories/`, sin contaminar servicios ni routers.
2. Se usa la librería **`bcrypt` directamente** en `core/security.py`, con truncado explícito a
   72 bytes (límite real de bcrypt que, desde la versión 4, lanza error si se supera) — otro
   detalle que la IA omitía.

### Caso 4 (menor) — Redirecciones 307 por la barra final

**Qué generó la IA.** Definió las rutas de colección como `@router.get("/")` bajo un `prefix`.
Con FastAPI eso registra `/api/productos/` y una petición a `/api/productos` (sin barra, que es
justo la que hace el frontend) responde **307 Temporary Redirect**, lo que en algunos clientes
rompe peticiones `POST`/`DELETE`.

**Corrección manual.** Las rutas de colección se declaran con path vacío (`@router.get("")`),
de modo que la URL exacta sin barra final es la registrada y no hay redirecciones.

---

## 4. Conclusiones

La IA fue muy útil para **acelerar** el andamiaje y resolver dudas puntuales de sintaxis, pero
**no produjo un backend correcto “a la primera”**: tendió a (a) centralizar todo en un archivo,
(b) cometer errores sutiles de seguridad y de API que habrían roto el frontend, y (c) proponer
atajos prohibidos por la práctica (persistencia en memoria). El valor real estuvo en **revisar
críticamente** cada sugerencia con los conceptos de la asignatura —separación de
responsabilidades, mínimo privilegio, semántica HTTP y patrón repositorio— y en **verificar con
pruebas** que el contrato seguía siendo compatible con el frontend de la Práctica 1.
