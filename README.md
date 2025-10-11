# Ecommerce IA API

## Descripción

Esta es una API RESTful para una plataforma de comercio electrónico, construida con FastAPI. La característica principal de este backend es el uso de Inteligencia Artificial (a través de la API de Google Gemini) para enriquecer los datos de los productos. Cuando un vendedor crea un nuevo producto, la API genera automáticamente una descripción de marketing mejorada y una imagen representativa del producto.

## Características

-   **Gestión de Vendedores**: Registro y autenticación de vendedores.
-   **Autenticación Segura**: Implementación de JSON Web Tokens (JWT) para proteger los endpoints.
-   **Creación de Productos Asistida por IA**:
    -   Generación automática de descripciones de productos optimizadas para la venta.
    -   Generación de imágenes de productos a partir de un nombre y descripción.
-   **Gestión de Productos**: Los vendedores pueden listar los productos que han creado.
-   **Arquitectura Asíncrona**: Uso de `async` y `await` para operaciones que consumen tiempo (llamadas a la IA), asegurando que la API no se bloquee.

## Tecnologías Utilizadas

-   **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Base de Datos**: [SQLAlchemy](https://www.sqlalchemy.org/) para el ORM (diseñado para MySQL/MariaDB).
-   **Autenticación**: [python-jose](https://github.com/mpdavis/python-jose) para JWT, [passlib](https://passlib.readthedocs.io/en/stable/) y [argon2-cffi](https://argon2-cffi.readthedocs.io/en/stable/) para el hashing de contraseñas.
-   **Inteligencia Artificial**: [Google Gemini](https://ai.google.dev/) para la generación de texto e imágenes.
-   **Validación de Datos**: [Pydantic](https://docs.pydantic.dev/latest/).
-   **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/).

## Instalación y Configuración

Sigue estos pasos para levantar un entorno de desarrollo local.

### 1. Prerrequisitos

-   Python 3.10 o superior.
-   Un servidor de base de datos MySQL o MariaDB en ejecución.

### 2. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd ecommerce-ia
```

### 3. Crear un Entorno Virtual

Es una buena práctica aislar las dependencias del proyecto.

```bash
python -m venv venv
source venv/bin/activate
# En Windows: venv\Scripts\activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

Crea un archivo llamado `.env` en la raíz del proyecto y añade las siguientes variables.

```ini
# Configuración de la Base de Datos
USERNAME="tu_usuario_de_bd"
PASSWORD="tu_contraseña_de_bd"
DBNAME="el_nombre_de_tu_bd"

# Claves para la API de IA
GEMINI_API_KEY="tu_api_key_de_google_gemini"

# Configuración de JWT
# Puedes generar una clave secreta con: openssl rand -hex 32
SECRET_KEY="tu_clave_secreta_para_jwt"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Ejecutar la Aplicación

Una vez configurado, puedes iniciar el servidor de desarrollo.

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Guía de la API

La documentación interactiva de la API (generada por Swagger UI) está disponible en `http://127.0.0.1:8000/docs`.

### Endpoints Principales

#### Autenticación

-   **`POST /register`**: Registra un nuevo vendedor.
    -   **Body**: `{ "email": "user@example.com", "password": "Password123!" }`
-   **`POST /login`**: Autentica a un vendedor y devuelve un token de acceso.
    -   **Body**: `x-www-form-urlencoded` con `username` (email) y `password`.
    -   **Respuesta**: `{ "access_token": "...", "token_type": "bearer" }`

#### Productos

-   **`POST /products`** `(Protegido)`: Crea un nuevo producto. La descripción y la imagen son generadas por IA.
    -   **Header**: `Authorization: Bearer <tu_token>`
    -   **Body**: `{ "name": "Mi Producto", "description": "Una breve descripción inicial.", "price": 29.99 }`
-   **`GET /products/me`** `(Protegido)`: Devuelve una lista de todos los productos creados por el vendedor autenticado.
    -   **Header**: `Authorization: Bearer <tu_token>`
