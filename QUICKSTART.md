# 🚀 Guía Rápida de Inicio

## Inicio Rápido (5 minutos)

### 1️⃣ Preparar el Entorno

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Configurar PostgreSQL

```powershell
# Agregar PostgreSQL al PATH (solo para esta sesión)
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"

# Si tienes PostgreSQL 18, usa:
# $env:Path += ";C:\Program Files\PostgreSQL\18\bin"

# Verificar que funciona
psql --version
```

### 3️⃣ Crear la Base de Datos (OPCIÓN A: Automático - RECOMENDADO)

```powershell
# Ejecutar el script automático (recomendado)
python setup_database.py
```

### 3️⃣ ALTERNATIVA: Crear la Base de Datos (OPCIÓN B: Manual)

```powershell
# Conectar a PostgreSQL
psql -U postgres
# Cuando pida contraseña, escribe: admin123 (la contraseña no se ve)
```

Dentro de PostgreSQL (verás `postgres=#`), copia y pega esto:

```sql
CREATE DATABASE technical_test;

\c technical_test

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'taskstatus') THEN
        CREATE TYPE taskstatus AS ENUM ('pending', 'in_progress', 'done');
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_id ON users(id);
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status taskstatus DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS ix_tasks_id ON tasks(id);
CREATE INDEX IF NOT EXISTS ix_tasks_title ON tasks(title);
CREATE INDEX IF NOT EXISTS ix_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS ix_tasks_created_at ON tasks(created_at);

\dt
\q
```

### 4️⃣ Crear el Usuario Inicial

```powershell
# Usar el nuevo script mejorado
python insert_user.py
```

### 5️⃣ Iniciar la Aplicación

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar uvicorn
uvicorn app.main:app --reload
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete
```

### 6️⃣ Probar la API

1. Abre: **http://127.0.0.1:8000/docs**
2. Busca el endpoint `POST /auth/login`
3. Click en "Try it out"
4. Ingresa:
   ```json
   {
     "email": "admin@example.com",
     "password": "admin123"
   }
   ```
5. Click en "Execute"
6. Copia el `access_token` de la respuesta
7. Click en el botón "Authorize" (🔒) arriba a la derecha
8. Pega el token como: `Bearer <tu_token>`
9. ¡Ya puedes usar todos los endpoints!

---

## ¿Problemas Comunes?

### ❌ "psql no se reconoce"
```powershell
# Agrega PostgreSQL al PATH
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"
psql --version
```

### ❌ "Connection refused"
PostgreSQL no está corriendo. Inicia el servicio:
```powershell
Start-Service postgresql-x64-16
```

### ❌ "Database does not exist"
Ejecuta:
```powershell
.\setup_db.ps1
```

### ❌ "relation does not exist"
Las tablas no se crearon. Ejecuta:
```powershell
python create_initial_user.py
```

### ❌ "Password authentication failed"
Edita el archivo `.env` y asegúrate de que `DB_PASSWORD` coincide con la contraseña de PostgreSQL.

---

## 📚 Estructura de Archivos

```
PruebaTecnica/
├── .env                      ← Configuración (NO compartir en Git)
├── requirements.txt          ← Dependencias de Python
├── README.md                 ← Guía completa
├── QUICKSTART.md            ← Este archivo
├── setup_db.ps1             ← Script de configuración automática
├── create_initial_user.py   ← Script para crear usuario
├── scripts/
│   └── init_database.sql   ← Script SQL manual
└── app/
    ├── main.py
    ├── api/
    ├── core/
    ├── db/
    ├── models/
    ├── schemas/
    └── services/
```

---

## 🎯 Próximos Pasos

- Leer [README.md](README.md) para documentación completa
- Explorar los endpoints en: http://127.0.0.1:8000/docs
- Revisar el código fuente en la carpeta `app/`

---

## 💡 Consejos

- **No compartas el archivo `.env`** en Git (añádelo a `.gitignore`)
- **Cambia `SECRET_KEY`** en `.env` para producción
- **Usa `--reload` solo en desarrollo**, no en producción
- **Leer la documentación completa** en [README.md](README.md) para entender los problemas que resolvimos

---

¡Bienvenido! Si tienes dudas, revisa el [README.md](README.md) 🚀
