#!/usr/bin/env python3
"""
Script de verificación de la instalación
Comprueba que todo está configurado correctamente
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def check_python_version():
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    return not (version.major < 3 or (version.major == 3 and version.minor < 9))

def check_dependencies():
    """Verificar dependencias instaladas"""
    required = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2',
        'pydantic',
        'pydantic_settings',
        'jose',
        'passlib'
    ]
    
    print("Checking dependencies:")
    all_ok = True
    
    for package in required:
        try:
            __import__(package)
            print(f"  {package}: ok")
        except ImportError:
            print(f"  {package}: missing")
            all_ok = False
    
    return all_ok

def check_env_file():
    """Verificar archivo .env"""
    env_file = Path('.env')
    print("\nChecking configuration (.env):")
    
    if env_file.exists():
        print("  ✓ .env existe")
        
        from app.core.config import settings
        
        checks = [
            ('DB_HOST', settings.DB_HOST),
            ('DB_PORT', settings.DB_PORT),
            ('DB_NAME', settings.DB_NAME),
            ('DB_USER', settings.DB_USER),
            ('SECRET_KEY', '***' if len(settings.SECRET_KEY) > 0 else 'VACIO'),
        ]
        
        for key, value in checks:
            display = value if key == 'SECRET_KEY' or len(str(value)) < 30 else f"{str(value)[:30]}..."
            print(f"    {key}: {display}")
        
        return True
    else:
        print("  ❌ .env no existe (ejecuta: copy .env.example .env)")
        return False

def check_database():
    """Verificar conexión a base de datos"""
    print("\nChecking database connection:")
    
    try:
        from app.db.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("  PostgreSQL: ok")
            return True
            
    except Exception as e:
        print(f"  DB error: {str(e)[:120]}")
        return False

def check_models():
    """Verificar que los modelos se cargan correctamente"""
    print("\nChecking models:")
    
    try:
        from app.models.user import User
        from app.models.task import Task
        print("  User model: ok")
        print("  Task model: ok")
        return True
    except Exception as e:
        print(f"  Model error: {e}")
        return False

def main():
    print("Installation check")
    checks = [
        ("Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Configuración", check_env_file),
        ("Modelos", check_models),
        ("Base de datos", check_database),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error verificando {name}: {e}")
            results.append((name, False))
    
    for name, result in results:
        print(f"{name}: {'OK' if result else 'FAIL'}")
    return all(result for _, result in results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
