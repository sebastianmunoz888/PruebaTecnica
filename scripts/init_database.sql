-- Script de Inicialización de Base de Datos
-- Technical Test API - FastAPI
-- 
-- Ejecución:
-- psql -U postgres -f scripts/init_database.sql
--

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS technical_test;

-- Conectar a la nueva base de datos
\c technical_test

-- Crear el tipo ENUM para estados de tareas
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'taskstatus') THEN
        CREATE TYPE taskstatus AS ENUM ('pending', 'in_progress', 'done');
    END IF;
END $$;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_id ON users(id);
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- Crear tabla de tareas
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

-- Mostrar información
\dt

SELECT 'Base de datos configurada correctamente' AS Status;
