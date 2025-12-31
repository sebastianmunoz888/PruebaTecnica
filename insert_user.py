#!/usr/bin/env python3
"""
Insertar usuario inicial directamente en la base de datos
Usa bcrypt directamente para evitar problemas de compatibilidad
"""

import sys
from pathlib import Path
import bcrypt

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.db.database import SessionLocal
from app.models.user import User
from sqlalchemy import text


def insert_user_direct():
    """Insertar usuario usando SQL directo"""
    password = "admin123"
    email = "admin@example.com"
    
    # Generar hash con bcrypt
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    try:
        db = SessionLocal()
        
        # Verificar si el usuario ya existe
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User already exists: {email}")
            db.close()
            return True
        
        # Crear el usuario
        
        new_user = User(
            email=email,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.close()
        
        print(f"User created: {email}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    success = insert_user_direct()
    sys.exit(0 if success else 1)
