# 🚀 API REST con FastAPI y PostgreSQL - Guía Completa

## 📖 Historia de Este Proyecto

Este proyecto es una API REST desarrollada con FastAPI que gestiona tareas (To-Do List) con autenticación JWT. Durante el desarrollo nos encontramos con varios desafíos que documentamos aquí para que otros desarrolladores no pasen por lo mismo.

---

## 🐛 Los Problemas Que Encontramos (Y Cómo Los Resolvimos)

### Problema #1: "psql no se reconoce como comando"

**¿Qué pasó?**
Cuando intentamos usar PostgreSQL desde la terminal, Windows no sabía dónde encontrarlo.

**¿Por qué pasó?**
PostgreSQL se instaló en `C:\Program Files\PostgreSQL\18\bin`, pero esta ruta no estaba en el PATH de Windows.

**Solución:**
```powershell
# Agregar PostgreSQL al PATH (temporal, solo para esta sesión)
$env:Path += ";C:\Program Files\PostgreSQL\18\bin"

# Para hacerlo permanente: Sistema > Configuración avanzada > Variables de entorno > Path
```

---

### Problema #2: "Docker no está disponible"

**¿Qué pasó?**
El README original decía que usáramos Docker, pero Docker no estaba instalado.

**¿Por qué pasó?**
Docker es opcional. Si tienes PostgreSQL instalado localmente, no necesitas Docker.

**Solución:**
Usamos PostgreSQL instalado directamente en Windows en lugar de Docker. Ambas opciones son válidas.

---

### Problema #3: "no existe la base de datos technical_test"

**¿Qué pasó?**
La aplicación intentaba conectarse a una base de datos que no existía.

**¿Por qué pasó?**
Aunque teníamos código para crear la base de datos automáticamente (`init_db.py`), el evento `lifespan` de FastAPI no se estaba ejecutando correctamente con `--reload`.

**Solución:**
Creamos la base de datos manualmente:
```sql
psql -U postgres
CREATE DATABASE technical_test;
\q
```

---

### Problema #4: "no existe la relación users"

**¿Qué pasó?**
La base de datos existía, pero las tablas no.

**¿Por qué pasó?**
Dos razones:
1. El evento `lifespan` no se ejecutaba con uvicorn `--reload`
2. El modelo `Task` usa un tipo ENUM con `create_type=False`, lo que significa que SQLAlchemy **no crea** el tipo ENUM automáticamente

**Solución:**
Creamos las tablas y el tipo ENUM manualmente en PostgreSQL.

---

### Problema #5: "La contraseña no se ve cuando escribo"

**¿Qué pasó?**
Al usar `psql` y pedir contraseña, parecía que no estaba escribiendo nada.

**¿Por qué pasó?**
Es una característica de seguridad de PostgreSQL. La contraseña se captura pero no se muestra.

**Solución:**
Simplemente escribir la contraseña (aunque no la veas) y presionar Enter.

---

## ✅ Instalación Paso a Paso (La Forma Correcta)

### Requisitos Previos
- ✅ Python 3.11.8
- ✅ PostgreSQL 16+ instalado
- ✅ Git

### Paso 1: Clonar y Preparar el Entorno

```powershell
# Clonar el repositorio
git clone <tu-repositorio>
cd PruebaTecnica

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Configurar PostgreSQL en el PATH

```powershell
# Agregar PostgreSQL al PATH (temporal)
$env:Path += ";C:\Program Files\PostgreSQL\18\bin"

# Verificar que funciona
psql --version
```

### Paso 3: Crear el Archivo .env

Crea un archivo `.env` en la raíz del proyecto con este contenido:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=technical_test
DB_USER=postgres
DB_PASSWORD=admin123
SECRET_KEY=clave_magica_123_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
INITIAL_USER_EMAIL=admin@example.com
INITIAL_USER_PASSWORD=admin123
```

**⚠️ IMPORTANTE:** Cambia `DB_PASSWORD` por la contraseña que configuraste al instalar PostgreSQL.

### Paso 4: Crear la Base de Datos y las Tablas

```powershell
# Conectar a PostgreSQL
psql -U postgres
# Contraseña: admin123 (o la que hayas configurado)
```

Dentro de PostgreSQL (`postgres=#`), ejecuta:

```sql
-- Crear la base de datos
CREATE DATABASE technical_test;

-- Conectar a la nueva base de datos
\c technical_test

-- Crear el tipo ENUM para estados de tareas
CREATE TYPE taskstatus AS ENUM ('pending', 'in_progress', 'done');

-- Crear tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_users_id ON users(id);
CREATE INDEX ix_users_email ON users(email);

-- Crear tabla de tareas
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status taskstatus DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX ix_tasks_id ON tasks(id);
CREATE INDEX ix_tasks_title ON tasks(title);
CREATE INDEX ix_tasks_status ON tasks(status);
CREATE INDEX ix_tasks_created_at ON tasks(created_at);

-- Verificar que todo se creó correctamente
\dt

-- Salir
\q
```

### Paso 5: Crear el Usuario Inicial

```powershell
python -c "from app.db.database import SessionLocal; from app.models.user import User; from app.core.security import get_password_hash; db = SessionLocal(); user = User(email='admin@example.com', hashed_password=get_password_hash('admin123')); db.add(user); db.commit(); print('✓ Usuario admin@example.com creado exitosamente')"
```

### Paso 6: Iniciar la Aplicación

```powershell
uvicorn app.main:app --reload
```

Deberías ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using WatchFiles
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Paso 7: Probar la API

1. **Abrir la documentación:** http://127.0.0.1:8000/docs
2. **Hacer clic en "POST /auth/login"**
3. **Click en "Try it out"**
4. **Ingresar credenciales:**
   ```json
   {
     "email": "admin@example.com",
     "password": "admin123"
   }
   ```
5. **Click en "Execute"**
6. **Copiar el `access_token` de la respuesta**
7. **Click en el botón "Authorize" (🔓) arriba a la derecha**
8. **Pegar el token en el formato:** `Bearer <tu_token_aqui>`
9. **¡Ahora puedes usar todos los endpoints de tareas!**

---

## 📚 Estructura del Proyecto

```
PruebaTecnica/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada
│   ├── api/                    # Endpoints
│   │   ├── auth.py            # Login
│   │   └── tasks.py           # CRUD de tareas
│   ├── core/                   
│   │   ├── config.py          # Configuración (.env)
│   │   └── security.py        # JWT y passwords
│   ├── db/                     
│   │   ├── database.py        # Conexión a PostgreSQL
│   │   └── init_db.py         # Scripts de inicialización
│   ├── models/                 # Modelos de base de datos
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/                # Validación de datos
│   │   ├── user.py
│   │   └── task.py
│   └── services/               # Lógica de negocio
│       ├── auth_service.py
│       └── task_service.py
├── .env                        # Variables de entorno
├── requirements.txt            # Dependencias
└── README.md
```

---

## 🎯 Endpoints Disponibles

### 🔐 Autenticación

#### POST /auth/login
Obtener token de acceso

**Request:**
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### ✅ Tareas (Requieren Autenticación)

#### POST /tasks/
Crear nueva tarea

**Request:**
```json
{
  "title": "Completar proyecto",
  "description": "Terminar la API REST",
  "status": "in_progress"
}
```

#### GET /tasks/
Listar tareas con paginación

**Query Params:**
- `page`: Número de página (default: 1)
- `page_size`: Tamaño de página (default: 10, max: 100)

#### GET /tasks/{task_id}
Obtener una tarea específica

#### PUT /tasks/{task_id}
Actualizar una tarea

**Request:**
```json
{
  "title": "Nuevo título",
  "status": "done"
}
```

#### DELETE /tasks/{task_id}
Eliminar una tarea

---

## 🔧 Solución de Problemas Comunes

### Error: "Module not found"
```powershell
# Asegúrate de estar en el entorno virtual
.\venv\Scripts\activate

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "Connection refused" al conectar con PostgreSQL
```powershell
# Verificar que PostgreSQL está corriendo
Get-Service | Where-Object {$_.Name -like "*postgres*"}

# Si no está corriendo, iniciarlo
Start-Service postgresql-x64-16
```

### Error: "Authentication failed"
La contraseña en tu `.env` no coincide con la de PostgreSQL. Actualiza `DB_PASSWORD` en el archivo `.env`.

### Olvidé la contraseña de PostgreSQL
1. Busca el archivo `pg_hba.conf` en `C:\Program Files\PostgreSQL\XX\data\`
2. Cambia `md5` por `trust` temporalmente
3. Reinicia el servicio de PostgreSQL
4. Cambia la contraseña con: `ALTER USER postgres PASSWORD 'nueva_contraseña';`
5. Revierte los cambios en `pg_hba.conf`

---

## 🎓 Lecciones Aprendidas

### 1. **Uvicorn --reload y eventos de inicio**
El modo `--reload` de uvicorn crea un proceso hijo, lo que puede causar que los eventos de inicialización no se ejecuten como esperamos. Para desarrollo, es mejor crear las tablas manualmente o usar un script separado.

### 2. **SQLAlchemy y tipos ENUM**
Cuando usas `create_type=False` en un ENUM de SQLAlchemy, debes crear el tipo manualmente en PostgreSQL **antes** de crear las tablas.

### 3. **PATH en Windows**
Windows no encuentra comandos que no están en el PATH. Siempre verifica que las herramientas estén en el PATH o usa rutas absolutas.

### 4. **Docker es opcional**
No necesitas Docker para desarrollar. PostgreSQL local funciona perfectamente bien.

### 5. **Contraseñas en psql**
Las contraseñas no se muestran en la terminal por seguridad. Esto es normal.

---

## 🚀 Próximos Pasos / Mejoras

- [ ] Implementar tests con pytest
- [ ] Agregar relación User → Tasks (cada usuario sus tareas)
- [ ] Implementar filtros y búsqueda en tareas
- [ ] Rate limiting para prevenir abuso
- [ ] Dockerizar la aplicación completa
- [ ] CI/CD con GitHub Actions
- [ ] Hacer que `init_db.py` funcione automáticamente

---

## 💡 Consejos para Producción

1. **Nunca uses `--reload` en producción** (solo para desarrollo)
2. **Cambia `SECRET_KEY`** a algo seguro y aleatorio
3. **Usa variables de entorno** para secretos (nunca en el código)
4. **Configura CORS** apropiadamente (no uses `"*"`)
5. **Usa HTTPS** siempre
6. **Implementa rate limiting**
7. **Monitorea tu aplicación** (logs, métricas)
8. **Usa Alembic** para migraciones de base de datos

---

## 👤 Autor

Desarrollado como prueba técnica para posición de Backend Developer Python.

**Tecnologías:** Python 3.11, FastAPI, PostgreSQL, SQLAlchemy, JWT, Bcrypt

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 🙏 Agradecimientos

A todos los que ayudaron a resolver los problemas de configuración y deployment. Los errores son parte del aprendizaje. 💪
