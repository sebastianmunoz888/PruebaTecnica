# Script de Inicialización de la Base de Datos - Technical Test API
# Este script configura PostgreSQL automáticamente

param(
    [string]$PostgresPath = "C:\Program Files\PostgreSQL\16\bin",
    [string]$DBUser = "postgres",
    [string]$DBPassword = "admin123",
    [string]$DBName = "technical_test"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Inicializador de Base de Datos" -ForegroundColor Yellow
Write-Host "Technical Test API - FastAPI" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Paso 1: Verificar que PostgreSQL está instalado
Write-Host "[Paso 1] Verificando PostgreSQL..." -ForegroundColor Yellow
if (-Not (Test-Path $PostgresPath)) {
    Write-Host "❌ PostgreSQL no encontrado en: $PostgresPath" -ForegroundColor Red
    Write-Host "Por favor, instala PostgreSQL o especifica la ruta correcta." -ForegroundColor Red
    Write-Host "`nEjemplo: .\setup_db.ps1 -PostgresPath 'C:\Program Files\PostgreSQL\18\bin'" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ PostgreSQL encontrado" -ForegroundColor Green

# Paso 2: Agregar PostgreSQL al PATH
Write-Host "`n[Paso 2] Configurando PATH..." -ForegroundColor Yellow
$env:Path += ";$PostgresPath"
Write-Host "✓ PATH configurado" -ForegroundColor Green

# Paso 3: Verificar conexión
Write-Host "`n[Paso 3] Verificando conexión a PostgreSQL..." -ForegroundColor Yellow
try {
    $result = psql -U $DBUser -h localhost -l 2>&1
    if ($result -like "*technical_test*") {
        Write-Host "✓ Base de datos 'technical_test' ya existe" -ForegroundColor Green
        $dbExists = $true
    } else {
        Write-Host "ℹ Base de datos 'technical_test' no existe aún" -ForegroundColor Cyan
        $dbExists = $false
    }
} catch {
    Write-Host "❌ No se pudo conectar a PostgreSQL" -ForegroundColor Red
    Write-Host "Asegúrate de que el servicio PostgreSQL esté corriendo" -ForegroundColor Red
    Write-Host "`nComando para iniciar PostgreSQL:" -ForegroundColor Yellow
    Write-Host "Start-Service postgresql-x64-16" -ForegroundColor White
    exit 1
}

# Paso 4: Crear la base de datos si no existe
if (-Not $dbExists) {
    Write-Host "`n[Paso 4] Creando base de datos..." -ForegroundColor Yellow
    $sqlScript = @"
CREATE DATABASE $DBName;
"@
    
    $sqlScript | psql -U $DBUser -h localhost 2>&1 | ForEach-Object {
        if ($_ -like "*CREATE DATABASE*" -or $_ -like "*already exists*") {
            Write-Host "✓ Base de datos '$DBName' creada" -ForegroundColor Green
        }
    }
}

# Paso 5: Crear el tipo ENUM y las tablas
Write-Host "`n[Paso 5] Creando tablas y tipos..." -ForegroundColor Yellow

$sqlScript = @"
\c $DBName

-- Crear el tipo ENUM si no existe
DO `$`$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'taskstatus') THEN
        CREATE TYPE taskstatus AS ENUM ('pending', 'in_progress', 'done');
    END IF;
END `$`$;

-- Crear tabla users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_id ON users(id);
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- Crear tabla tasks
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
"@

$sqlScript | psql -U $DBUser -h localhost 2>&1 | ForEach-Object {
    if ($_ -like "*CREATE TABLE*" -or $_ -like "*already exists*") {
        Write-Host "✓ Tablas y tipos creados" -ForegroundColor Green
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✓ Base de datos configurada correctamente" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nProximos pasos:" -ForegroundColor Yellow
Write-Host "1. Activar el entorno virtual: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Instalar dependencias: pip install -r requirements.txt" -ForegroundColor White
Write-Host "3. Iniciar la aplicación: uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "4. Abrir: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host ""
