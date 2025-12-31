#!/usr/bin/env python3
"""
Script para crear las tablas en la base de datos
Ejecutar con: python setup_database.py
"""

import sys
from pathlib import Path
from sqlalchemy import text, create_engine, inspect

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.core.config import settings
from app.db.database import Base, engine


def table_exists(table_name):
    """Verificar si una tabla existe"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def create_enum_type():
    """Crear el tipo ENUM taskstatus"""
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                DO $$ BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'taskstatus') THEN
                        CREATE TYPE taskstatus AS ENUM ('pending', 'in_progress', 'done');
                    END IF;
                END $$;
            """))
            conn.commit()
        return True
    except Exception:
        return False


def create_tables():
    """Crear las tablas usando SQLAlchemy"""
    try:
        from app.models import user, task
        Base.metadata.create_all(bind=engine)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return 'users' in tables and 'tasks' in tables
    except Exception:
        return False


def create_indexes():
    """Crear los índices"""
    try:
        with engine.connect() as conn:
            indexes = [
                "CREATE INDEX IF NOT EXISTS ix_users_id ON users(id)",
                "CREATE INDEX IF NOT EXISTS ix_users_email ON users(email)",
                "CREATE INDEX IF NOT EXISTS ix_tasks_id ON tasks(id)",
                "CREATE INDEX IF NOT EXISTS ix_tasks_title ON tasks(title)",
                "CREATE INDEX IF NOT EXISTS ix_tasks_status ON tasks(status)",
                "CREATE INDEX IF NOT EXISTS ix_tasks_created_at ON tasks(created_at)",
            ]
            for idx in indexes:
                conn.execute(text(idx))
            conn.commit()
        return True
    except Exception:
        return False


def main():
    # Minimal output
    
    print(f"Configuring DB {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    try:
        if not create_enum_type():
            pass
        if not create_tables():
            raise Exception("Tables creation failed")
        create_indexes()
        print("Database configured")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
