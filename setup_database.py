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
        print("✓ Tipo ENUM 'taskstatus' creado (o ya existe)")
        return True
    except Exception as e:
        print(f"❌ Error al crear ENUM: {e}")
        return False


def create_tables():
    """Crear las tablas usando SQLAlchemy"""
    try:
        # Importar modelos para registrarlos en Base
        from app.models import user, task
        
        # Crear las tablas
        Base.metadata.create_all(bind=engine)
        
        # Verificar que se crearon
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'users' in tables and 'tasks' in tables:
            print("✓ Tabla 'users' creada")
            print("✓ Tabla 'tasks' creada")
            return True
        else:
            print("❌ Las tablas no se crearon correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        import traceback
        traceback.print_exc()
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
        print("✓ Índices creados")
        return True
    except Exception as e:
        print(f"❌ Error al crear índices: {e}")
        return False


def main():
    print("\n" + "=" * 70)
    print("CONFIGURACIÓN DE BASE DE DATOS")
    print("Technical Test API - FastAPI")
    print("=" * 70 + "\n")
    
    print(f"Conectando a: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    
    try:
        # Paso 1: Crear ENUM
        print("\n[Paso 1] Creando tipo ENUM...")
        if not create_enum_type():
            print("⚠ Continuando sin embargo...")
        
        # Paso 2: Crear tablas
        print("\n[Paso 2] Creando tablas...")
        if not create_tables():
            raise Exception("No se pudieron crear las tablas")
        
        # Paso 3: Crear índices
        print("\n[Paso 3] Creando índices...")
        if not create_indexes():
            print("⚠ No se pudieron crear todos los índices, pero continuamos")
        
        print("\n" + "=" * 70)
        print("✓ Base de datos configurada correctamente")
        print("=" * 70)
        print("\nProximos pasos:")
        print("  1. Crear usuario inicial: python create_initial_user.py")
        print("  2. Iniciar la aplicación: uvicorn app.main:app --reload")
        print("=" * 70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
