#!/usr/bin/env python3
"""
Script para crear el usuario inicial en la base de datos.
Uso: python create_initial_user.py
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings


def main():
    print("\n" + "=" * 70)
    print("Script de Creación de Usuario Inicial")
    print("Technical Test API - FastAPI")
    print("=" * 70 + "\n")
    
    try:
        db = SessionLocal()
        
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(
            User.email == settings.INITIAL_USER_EMAIL
        ).first()
        
        if existing_user:
            print(f"ℹ El usuario '{settings.INITIAL_USER_EMAIL}' ya existe")
            print("\nCredenciales:")
            print(f"  Email:    {settings.INITIAL_USER_EMAIL}")
            print(f"  Password: {settings.INITIAL_USER_PASSWORD}")
            return True
        
        # Crear el usuario
        print(f"Creando usuario: {settings.INITIAL_USER_EMAIL}")
        hashed_password = get_password_hash(settings.INITIAL_USER_PASSWORD)
        
        initial_user = User(
            email=settings.INITIAL_USER_EMAIL,
            hashed_password=hashed_password
        )
        
        db.add(initial_user)
        db.commit()
        db.close()
        
        print("\n" + "=" * 70)
        print("✓ Usuario creado exitosamente")
        print("=" * 70)
        print("\nCredenciales:")
        print(f"  Email:    {settings.INITIAL_USER_EMAIL}")
        print(f"  Password: {settings.INITIAL_USER_PASSWORD}")
        print("\nAhora puedes iniciar la aplicación con:")
        print("  uvicorn app.main:app --reload")
        print("\nY acceder a la documentación en:")
        print("  http://127.0.0.1:8000/docs")
        print("=" * 70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error al crear el usuario: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
