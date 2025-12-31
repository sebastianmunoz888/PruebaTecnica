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
    # Minimal, non-verbose output
    try:
        db = SessionLocal()
        
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.email == settings.INITIAL_USER_EMAIL).first()
        if existing_user:
            print(f"User already exists: {settings.INITIAL_USER_EMAIL}")
            return True
        
        # Crear el usuario
        hashed_password = get_password_hash(settings.INITIAL_USER_PASSWORD)
        
        initial_user = User(
            email=settings.INITIAL_USER_EMAIL,
            hashed_password=hashed_password
        )
        
        db.add(initial_user)
        db.commit()
        db.close()
        
        print("User created: {}".format(settings.INITIAL_USER_EMAIL))
        
        return True
        
    except Exception as e:
        print(f"Error creating user: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
